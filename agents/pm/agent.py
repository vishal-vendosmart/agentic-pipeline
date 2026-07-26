#!/usr/bin/env python3
"""
Project Manager Agent - OpenClaw Integration
Role: Strategic orchestrator for agentic pipeline
Integration: Uses Linear MCP tools + spawns Hermes agents via exec
"""

import os
import json
import subprocess
import re
from datetime import datetime
from typing import Dict, List

class ProjectManagerAgent:
    def __init__(self):
        self.linear_team_id = os.getenv('LINEAR_TEAM_ID', '6708e155-7999-4102-994c-88e6cdc1180f')
        self.workspace = os.getenv('OPENCLAW_WORKSPACE', '/root/.openclaw')
        self.hermes_agents_dir = f'{self.workspace}/hermes-agents'
    
    def spawn_researcher(self, seed_keywords: List[str], vertical: str = 'A') -> Dict:
        """Spawn Researcher Hermes agent via exec"""
        
        print(f"🔍 Spawning Researcher agent for Vertical {vertical}")
        print(f"   Seed keywords: {seed_keywords}")
        
        agent_script = f'{self.hermes_agents_dir}/researcher-vertical-a/agent.py'
        
        result = subprocess.run(
            ['python3', agent_script],
            capture_output=True,
            text=True,
            env={**os.environ, 'VERTICAL': vertical}
        )
        
        # Extract JSON from output (last JSON object)
        try:
            # Find JSON in stdout
            json_match = re.search(r'\{[^{}]*\}', result.stdout, re.DOTALL)
            if json_match:
                output = json.loads(json_match.group())
                print(f"   ✓ Researcher completed: {output.get('total_keywords', 0)} keywords")
                return {'success': True, 'agent': f'researcher-vertical-{vertical.lower()}', 'result': output}
            else:
                raise ValueError("No JSON found in output")
        except Exception as e:
            print(f"   ⚠ Parse error: {e}")
            print(f"   stdout: {result.stdout[:200]}")
            return {'success': False, 'error': f'Parse error: {e}', 'stdout': result.stdout[:500]}
    
    def create_linear_project(self, title: str, description: str) -> Dict:
        """Create Linear project using MCP tool"""
        print(f"📋 Creating Linear project: {title}")
        return {
            'success': True,
            'message': 'Project creation prepared (call linear_create_issue in OpenClaw)',
            'data': {'title': title, 'description': description, 'teamId': self.linear_team_id, 'priority': 'high'}
        }
    
    def update_linear_task(self, task_id: str, updates: Dict) -> Dict:
        """Update Linear task using MCP tool"""
        print(f"📝 Updating Linear task {task_id}")
        return {'success': True, 'message': f'Task update prepared for {task_id}', 'updates': updates}
    
    def run_content_pipeline(self, objective: str, seed_keywords: List[str]) -> Dict:
        """Full content generation pipeline"""
        
        print("=" * 60)
        print("🚀 Starting Content Generation Pipeline")
        print("=" * 60)
        
        project = self.create_linear_project(
            title=f"Content Generation - {datetime.now().strftime('%Y-%m')}",
            description=f"Automated content generation: {objective}"
        )
        
        researcher_result = self.spawn_researcher(seed_keywords)
        
        if not researcher_result.get('success'):
            return {'success': False, 'error': 'Researcher agent failed', 'details': researcher_result}
        
        task_update = self.update_linear_task('MAR-124', {
            'description': f"✅ Research Complete\n\n" +
                          f"**Keywords Discovered:** {researcher_result['result'].get('total_keywords', 0)}\n" +
                          f"- Primary: {researcher_result['result'].get('primary_count', 'N/A')}\n" +
                          f"- Long-tail: {researcher_result['result'].get('long_tail_count', 'N/A')}\n\n" +
                          f"**Next:** Writer agent can start"
        })
        
        print("\n" + "=" * 60)
        print("✅ Pipeline Complete")
        print("=" * 60)
        
        return {'success': True, 'project': project, 'researcher': researcher_result, 'task_update': task_update}

if __name__ == '__main__':
    pm = ProjectManagerAgent()
    result = pm.run_content_pipeline(
        objective="Generate 20 leads/month from manufacturing SMEs",
        seed_keywords=['AI procurement software', 'manufacturing automation']
    )
    print("\n" + json.dumps(result, indent=2, default=str))
