#!/usr/bin/env python3
"""
PM orchestration CLI/utility — NOT the agent itself.
The real PM agent is the openclaw agent `pm-agent` (profile `pm`).
This script is a deterministic helper: real Linear GraphQL API calls +
spawns the researcher/writer UTILITIES (not agents) via exec for batch runs.
The openclaw pm-agent orchestrates live agents via sessions_spawn; this
script is its CLI/batch counterpart.
"""

import os
import json
import subprocess
import requests
from datetime import datetime
from typing import Dict, List, Optional

LINEAR_API_URL = 'https://api.linear.app/graphql'
ENV_FILE = '/root/dev/agentic-pipeline/.env'


def load_env():
    """Load environment variables from .env file"""
    if os.path.exists(ENV_FILE):
        with open(ENV_FILE) as f:
            for line in f:
                line = line.strip()
                if '=' in line and not line.startswith('#'):
                    k, v = line.split('=', 1)
                    os.environ.setdefault(k, v)


class LinearClient:
    """Real Linear GraphQL API client. No simulation."""

    def __init__(self):
        load_env()
        self.api_key = os.environ['LINEAR_API_KEY']  # fail fast if missing
        self.team_id = os.getenv('LINEAR_TEAM_ID', '6708e155-7999-4102-994c-88e6cdc1180f')

    def _gql(self, query: str, variables: Optional[Dict] = None) -> Dict:
        r = requests.post(
            LINEAR_API_URL,
            headers={'Content-Type': 'application/json', 'Authorization': self.api_key},
            json={'query': query, 'variables': variables or {}},
            timeout=30,
        )
        r.raise_for_status()
        payload = r.json()
        if payload.get('errors'):
            raise RuntimeError(f"Linear API errors: {payload['errors']}")
        return payload['data']

    def create_project(self, name: str, description: str) -> Dict:
        data = self._gql(
            """mutation($input: ProjectCreateInput!) {
              projectCreate(input: $input) {
                success
                project { id name url }
              }
            }""",
            {'input': {'name': name, 'description': description, 'teamIds': [self.team_id]}},
        )
        res = data['projectCreate']
        if not res['success']:
            raise RuntimeError('projectCreate returned success=false')
        print(f"   ✓ Linear project created: {res['project']['name']} ({res['project']['url']})")
        return {'success': True, 'project': res['project']}

    def create_issue(self, title: str, description: str, priority: int = 1) -> Dict:
        data = self._gql(
            """mutation($input: IssueCreateInput!) {
              issueCreate(input: $input) {
                success
                issue { id identifier url title }
              }
            }""",
            {'input': {'teamId': self.team_id, 'title': title, 'description': description, 'priority': priority}},
        )
        res = data['issueCreate']
        if not res['success']:
            raise RuntimeError('issueCreate returned success=false')
        print(f"   ✓ Linear issue created: {res['issue']['identifier']} ({res['issue']['url']})")
        return {'success': True, 'issue': res['issue']}

    def get_issue(self, identifier: str) -> Dict:
        """Query issue by identifier (e.g. MAR-253). Real read."""
        data = self._gql(
            """query($id: String!) {
              issue(id: $id) {
                id identifier title description url
                state { name type }
              }
            }""",
            {'id': identifier},
        )
        issue = data.get('issue')
        if not issue:
            raise RuntimeError(f'Issue {identifier} not found')
        return {'success': True, 'issue': issue}

    def update_issue(self, identifier: str, description: Optional[str] = None,
                     state_name: Optional[str] = None) -> Dict:
        """Update issue description and/or state. Resolves identifier -> UUID first."""
        issue = self.get_issue(identifier)['issue']
        update_input: Dict = {}
        if description is not None:
            update_input['description'] = description
        if state_name is not None:
            states = self._gql(
                """query($teamId: String!) {
                  team(id: $teamId) { states { nodes { id name type } } }
                }""",
                {'teamId': self.team_id},
            )['team']['states']['nodes']
            match = next((s for s in states if s['name'].lower() == state_name.lower()), None)
            if not match:
                raise RuntimeError(f'State "{state_name}" not found in team states')
            update_input['stateId'] = match['id']
        if not update_input:
            return {'success': True, 'message': 'nothing to update'}

        data = self._gql(
            """mutation($id: String!, $input: IssueUpdateInput!) {
              issueUpdate(id: $id, input: $input) {
                success
                issue { id identifier url state { name } }
              }
            }""",
            {'id': issue['id'], 'input': update_input},
        )
        res = data['issueUpdate']
        if not res['success']:
            raise RuntimeError('issueUpdate returned success=false')
        print(f"   ✓ Linear issue updated: {res['issue']['identifier']} (state: {res['issue']['state']['name']})")
        return {'success': True, 'issue': res['issue']}

    def comment_on_issue(self, identifier: str, body: str, agent_name: str = 'PM Agent',
                          gateway_port: int = 18790) -> Dict:
        """Add a signed comment to a Linear issue. Every agent signs its comments
        so you can tell who said what (Linear API shows all as the API key owner).

        Comment format:
        ---
        **— <Agent Name>** (via gateway :<port>)

        <body with file links, Neo4j queries, results>
        """
        issue = self.get_issue(identifier)['issue']
        signed_body = f"---\n**— {agent_name}** (via gateway :{gateway_port})\n\n{body}"
        data = self._gql(
            """mutation($input: CommentCreateInput!) {
              commentCreate(input: $input) { success comment { id body } }
            }""",
            {'input': {'issueId': issue['id'], 'body': signed_body}},
        )
        res = data['commentCreate']
        if not res['success']:
            raise RuntimeError('commentCreate returned success=false')
        print(f"   ✓ Comment added to {identifier} (signed: {agent_name})")
        return {'success': True, 'comment': res['comment']}


class PMOrchestrator:
    def __init__(self):
        self.linear = LinearClient()
        self.workspace = os.getenv('OPENCLAW_WORKSPACE', '/root/.openclaw-pm')
        self.hermes_agents_dir = f'{self.workspace}/utilities'

    # ---------- A2A: cross-gateway agent-to-agent commands ----------

    def a2a_send(self, target_profile: str, target_agent: str, message: str, timeout: int = 300) -> Dict:
        """Send a real-time command to another agent's gateway and get its response.
        Uses: openclaw --profile <target> agent --agent <id> -m "..." --json
        This is cross-gateway A2A — PM talks to researcher-a/writer-a in real time."""
        print(f"📡 A2A → {target_agent} (profile {target_profile}): {message[:80]}...")
        result = subprocess.run(
            ['openclaw', '--profile', target_profile, 'agent',
             '--agent', target_agent, '-m', message, '--json'],
            capture_output=True, text=True, timeout=timeout
        )
        if result.returncode != 0:
            return {'success': False, 'error': result.stderr[:300], 'agent': target_agent}
        try:
            d = json.loads(result.stdout)
            r = d.get('result', d)
            txt = r.get('payloads', [{}])[0].get('text', '') if isinstance(r, dict) else str(r)
            print(f"   ✓ {target_agent} responded ({len(txt)} chars)")
            return {'success': True, 'agent': target_agent, 'response': txt}
        except Exception as e:
            return {'success': False, 'error': f'parse: {e}', 'stdout': result.stdout[:200], 'agent': target_agent}

    def command_researcher(self, message: str) -> Dict:
        """Real-time A2A command to Researcher-A agent (gateway :18793)."""
        return self.a2a_send('researcher-a', 'researcher-a', message)

    def command_writer(self, message: str) -> Dict:
        """Real-time A2A command to Writer-A agent (gateway :18794)."""
        return self.a2a_send('writer-a', 'writer-a', message)

    def spawn_researcher(self, seed_keywords: List[str], vertical: str = 'A') -> Dict:
        """Spawn Researcher Hermes agent via exec (real subprocess)"""

        print(f"🔍 Spawning Researcher agent for Vertical {vertical}")
        print(f"   Seed keywords: {seed_keywords}")

        agent_script = f'{self.hermes_agents_dir}/researcher-a/research.py'

        result = subprocess.run(
            ['python3', agent_script],
            capture_output=True,
            text=True,
            env={**os.environ, 'VERTICAL': vertical}
        )

        return self._parse_agent_output(result, f'researcher-a-utility')

    def spawn_writer(self, keyword: Optional[str] = None, vertical: str = 'A') -> Dict:
        """Spawn Writer Hermes agent via exec (real subprocess, independent agent)"""

        print(f"✍️  Spawning Writer agent for Vertical {vertical}")

        agent_script = f'{self.hermes_agents_dir}/writer-a/write_draft.py'
        cmd = ['python3', agent_script] + ([keyword] if keyword else [])

        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            env={**os.environ, 'VERTICAL': vertical}
        )

        return self._parse_agent_output(result, f'writer-a-utility')

    @staticmethod
    def _parse_agent_output(result, agent_name: str) -> Dict:
        """Extract trailing JSON object from agent stdout (supports nested JSON)."""
        try:
            stdout = result.stdout
            start = stdout.rfind('\n{')
            candidate = stdout[start + 1:] if start != -1 else stdout
            output = json.loads(candidate)
            print(f"   ✓ {agent_name} completed: {output.get('total_keywords', output.get('keyword', 'done'))}")
            return {'success': True, 'agent': agent_name, 'result': output}
        except Exception as e:
            print(f"   ⚠ Parse error: {e}")
            print(f"   stdout: {result.stdout[:200]}")
            return {'success': False, 'error': f'Parse error: {e}', 'stdout': result.stdout[:500]}

    def run_content_pipeline(self, objective: str, seed_keywords: List[str]) -> Dict:
        """Full content generation pipeline — all steps real"""

        print("=" * 60)
        print("🚀 Starting Content Generation Pipeline")
        print("=" * 60)

        # 1. Create a REAL tracking issue for this run
        run_title = f"Content Pipeline Run — {datetime.now().strftime('%Y-%m-%d %H:%M')}"
        run_desc = (f"**Objective:** {objective}\n\n"
                    f"**Seed keywords:** {', '.join(seed_keywords)}\n\n"
                    f"Status: researcher running…")
        tracker = self.linear.create_issue(run_title, run_desc, priority=1)
        tracker_id = tracker['issue']['identifier']

        # 2. Spawn researcher (real exec)
        researcher_result = self.spawn_researcher(seed_keywords)

        if not researcher_result.get('success'):
            self.linear.update_issue(
                tracker_id,
                description=run_desc + f"\n\n❌ **Researcher failed:** {researcher_result.get('error')}")
            return {'success': False, 'error': 'Researcher agent failed', 'details': researcher_result}

        # 3. Update the REAL Linear issue with verified results
        r = researcher_result['result']
        final_desc = (
            f"**Objective:** {objective}\n\n"
            f"✅ **Research Complete**\n\n"
            f"**Keywords Discovered:** {r.get('total_keywords', 0)}\n"
            f"- Primary: {r.get('primary_count', 'N/A')}\n"
            f"- Long-tail: {r.get('long_tail_count', 'N/A')}\n\n"
            f"**Stored:** Neo4j (agentic-pipeline-neo4j)\n\n"
            f"**Next:** Writer agent can start"
        )
        update = self.linear.update_issue(tracker_id, description=final_desc)

        print("\n" + "=" * 60)
        print("✅ Pipeline Complete")
        print("=" * 60)

        return {'success': True, 'tracker': tracker, 'researcher': researcher_result, 'update': update}


if __name__ == '__main__':
    pm = PMOrchestrator()
    result = pm.run_content_pipeline(
        objective="Generate 20 leads/month from manufacturing SMEs",
        seed_keywords=['AI procurement software', 'manufacturing automation']
    )
    print("\n" + json.dumps(result, indent=2, default=str))
