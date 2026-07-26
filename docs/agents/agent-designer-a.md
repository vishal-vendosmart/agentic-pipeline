# Agent Specification: Designer (ProQSmart)

**ID:** `designer-vertical-a`  
**Role:** UI/UX Design + Code Generation  
**Vertical:** ProQSmart (Vertical A)  
**Primary Model:** `ollama-cloud/minimax-m3`  
**Workspace:** `/root/.openclaw/workspace-designer-a/`

---

## 1. Purpose

Generate production-ready React/Tailwind code for landing pages and blog posts by integrating approved content with design components. Uses OpenDesign API for component generation and customizes for brand alignment.

---

## 2. Inputs

### 2.1 From Project Manager

**Format:** `sessions_spawn` task

**Example:**
```json
{
  "task": "Design 5 landing pages for ProQSmart",
  "params": {
    "objective": "Generate 20 leads/month from manufacturing SMEs",
    "vertical": "A",
    "linearTaskId": "MAR-127",
    "contentFiles": [
      "workspace-vertical-a/drafts/2026-07-26-ai-procurement.md",
      "workspace-vertical-a/drafts/2026-07-26-landing-page.md"
    ],
    "brandGuidelines": {
      "primaryColor": "#1e3a8a",
      "secondaryColor": "#f59e0b",
      "mood": "professional, trustworthy"
    }
  }
}
```

### 2.2 From Writer Agent

**Format:** Markdown files in workspace

**Files:**
- Blog posts: `/root/.openclaw/workspace-vertical-a/drafts/*.md`
- Landing pages: `/root/.openclaw/workspace-vertical-a/drafts/*-landing.md`

**Content Structure:**
```markdown
---
title: "AI Procurement Software Guide"
slug: "ai-procurement-guide"
targetKeyword: "AI procurement software"
wordCount: 2450
---

# AI Procurement Software: Complete Guide

[Introduction...]

[Body sections...]

[Call to Action...]
```

### 2.3 From Knowledge Graph

**Format:** Neo4j Cypher queries

**Queries:**
```cypher
// Get brand guidelines
MATCH (b:Brand {vertical: "A"})
RETURN b.primaryColor, b.secondaryColor, b.mood

// Get design preferences
MATCH (p:DesignPreference {vertical: "A"})
RETURN p.componentStyle, p.layoutType
```

---

## 3. Outputs

### 3.1 To Workspace

**Files Created:**
- `/root/.openclaw/workspace-designer-a/pages/homepage.tsx`
- `/root/.openclaw/workspace-designer-a/pages/landing-ai-procurement.tsx`
- `/root/.openclaw/workspace-designer-a/pages/blog-post.tsx`
- `/root/.openclaw/workspace-designer-a/components/HeroSection.tsx`
- `/root/.openclaw/workspace-designer-a/components/FeatureGrid.tsx`
- `/root/.openclaw/workspace-designer-a/components/LeadForm.tsx`
- `/root/.openclaw/workspace-designer-a/styles/globals.css`

**Example - Landing Page Component:**
```tsx
import { Button } from "@/components/ui/button";
import { Card, CardContent } from "@/components/ui/card";
import { LeadForm } from "@/components/lead-form";

export default function AIProcurementLanding() {
  return (
    <div className="min-h-screen bg-white">
      {/* Hero Section */}
      <section className="py-20 bg-gradient-to-r from-blue-900 to-blue-800">
        <div className="container mx-auto px-4">
          <h1 className="text-5xl font-bold text-white mb-6">
            Reduce Procurement Costs by 30% with AI
          </h1>
          <p className="text-xl text-blue-100 mb-8">
            ProQSmart helps manufacturing SMEs automate procurement and build stronger supplier relationships.
          </p>
          <Button size="lg" className="bg-white text-blue-900 hover:bg-blue-50">
            Request Demo
          </Button>
        </div>
      </section>

      {/* Features Grid */}
      <section className="py-16">
        <div className="container mx-auto px-4">
          <h2 className="text-3xl font-bold text-center mb-12">
            Key Benefits
          </h2>
          <div className="grid md:grid-cols-3 gap-8">
            <Card>
              <CardContent className="pt-6">
                <h3 className="text-xl font-semibold mb-2">
                  30% Cost Reduction
                </h3>
                <p className="text-gray-600">
                  AI-powered supplier matching finds the best prices automatically.
                </p>
              </CardContent>
            </Card>
            
            <Card>
              <CardContent className="pt-6">
                <h3 className="text-xl font-semibold mb-2">
                  80% Time Savings
                </h3>
                <p className="text-gray-600">
                  Automate purchase orders, approvals, and payments.
                </p>
              </CardContent>
            </Card>
            
            <Card>
              <CardContent className="pt-6">
                <h3 className="text-xl font-semibold mb-2">
                  Real-Time Analytics
                </h3>
                <p className="text-gray-600">
                  Track spending, supplier performance, and savings in one dashboard.
                </p>
              </CardContent>
            </Card>
          </div>
        </div>
      </section>

      {/* Lead Form */}
      <section className="py-16 bg-gray-50">
        <div className="container mx-auto px-4">
          <h2 className="text-3xl font-bold text-center mb-8">
            Get Started Today
          </h2>
          <LeadForm 
            action="/api/leads"
            fields={['email', 'company', 'phone']}
            submitText="Request Demo"
          />
        </div>
      </section>
    </div>
  );
}
```

**Example - Component Library:**
```tsx
// components/HeroSection.tsx
import { Button } from "@/components/ui/button";

interface HeroSectionProps {
  title: string;
  subtitle: string;
  ctaText: string;
  ctaLink: string;
  backgroundImage?: string;
}

export function HeroSection({ title, subtitle, ctaText, ctaLink }: HeroSectionProps) {
  return (
    <section className="py-20 bg-gradient-to-r from-blue-900 to-blue-800">
      <div className="container mx-auto px-4">
        <h1 className="text-5xl font-bold text-white mb-6">
          {title}
        </h1>
        <p className="text-xl text-blue-100 mb-8">
          {subtitle}
        </p>
        <Button size="lg" className="bg-white text-blue-900 hover:bg-blue-50" asChild>
          <a href={ctaLink}>{ctaText}</a>
        </Button>
      </div>
    </section>
  );
}

// components/FeatureGrid.tsx
import { Card, CardContent } from "@/components/ui/card";

interface Feature {
  title: string;
  description: string;
  icon?: string;
}

interface FeatureGridProps {
  features: Feature[];
  columns?: 2 | 3 | 4;
}

export function FeatureGrid({ features, columns = 3 }: FeatureGridProps) {
  return (
    <section className="py-16">
      <div className="container mx-auto px-4">
        <div className={`grid md:grid-cols-${columns} gap-8`}>
          {features.map((feature, index) => (
            <Card key={index}>
              <CardContent className="pt-6">
                <h3 className="text-xl font-semibold mb-2">
                  {feature.title}
                </h3>
                <p className="text-gray-600">
                  {feature.description}
                </p>
              </CardContent>
            </Card>
          ))}
        </div>
      </div>
    </section>
  );
}

// components/LeadForm.tsx
interface LeadFormProps {
  action: string;
  fields: string[];
  submitText: string;
}

export function LeadForm({ action, fields, submitText }: LeadFormProps) {
  return (
    <form action={action} className="max-w-md mx-auto">
      {fields.includes('email') && (
        <div className="mb-4">
          <label htmlFor="email" className="block text-sm font-medium mb-2">
            Email
          </label>
          <input
            type="email"
            id="email"
            name="email"
            required
            className="w-full px-4 py-2 border border-gray-300 rounded-md"
          />
        </div>
      )}
      
      {fields.includes('company') && (
        <div className="mb-4">
          <label htmlFor="company" className="block text-sm font-medium mb-2">
            Company
          </label>
          <input
            type="text"
            id="company"
            name="company"
            required
            className="w-full px-4 py-2 border border-gray-300 rounded-md"
          />
        </div>
      )}
      
      {fields.includes('phone') && (
        <div className="mb-4">
          <label htmlFor="phone" className="block text-sm font-medium mb-2">
            Phone
          </label>
          <input
            type="tel"
            id="phone"
            name="phone"
            className="w-full px-4 py-2 border border-gray-300 rounded-md"
          />
        </div>
      )}
      
      <Button type="submit" className="w-full">
        {submitText}
      </Button>
    </form>
  );
}
```

### 3.2 To Gamma.app (Infographics)

**Format:** API requests for infographic generation

**Example:**
```python
POST https://public-api.gamma.app/v1/generations

{
  "title": "AI Procurement Benefits Infographic",
  "content": "30% cost reduction, 80% time savings, real-time analytics",
  "format": "presentation_16:9",
  "style": "professional"
}
```

### 3.3 To Linear

**Updates:**
```graphql
mutation {
  updateIssue(
    id: "MAR-127"
    input: {
      description: """
      ✅ Design Complete
      
      **Pages Created:** 5
      - Homepage: ✅
      - Landing pages: 3
      - Blog template: 1
      
      **Components Generated:** 8
      - HeroSection
      - FeatureGrid
      - LeadForm
      - CTA Banner
      - TestimonialCarousel
      - LogoGrid
      - FAQ Section
      - Footer
      
      **Integration:**
      - Content integrated: ✅
      - Brand colors applied: ✅
      - CTAs aligned with objective: ✅
      
      **Infographics:** 3 generated via Gamma.app
      
      **Next:** SEO agent can optimize meta tags
      """
      stateId: "done"
    }
  ) {
    success
  }
}
```

---

## 4. Behaviors

### 4.1 Content Analysis Workflow

**Step 1: Parse Markdown Content**
```python
import frontmatter

def parse_content(filepath: str) -> dict:
    with open(filepath) as f:
        post = frontmatter.load(f)
    
    return {
        'title': post.get('title', 'Untitled'),
        'slug': post.get('slug', ''),
        'content': post.content,
        'wordCount': post.get('wordCount', 0),
        'targetKeyword': post.get('targetKeyword', ''),
        'pageType': post.get('pageType', 'blog')
    }
```

**Step 2: Identify Page Sections**
```python
def identify_sections(content: str) -> list:
    sections = []
    
    # Detect section headers
    lines = content.split('\n')
    current_section = []
    current_header = None
    
    for line in lines:
        if line.startswith('# '):
            if current_header:
                sections.append({
                    'header': current_header,
                    'content': '\n'.join(current_section)
                })
            current_header = line[2:]
            current_section = []
        else:
            current_section.append(line)
    
    return sections
```

**Step 3: Determine Component Needs**
```python
def determine_components(page_type: str, sections: list) -> list:
    components = []
    
    if page_type == 'landing':
        components = [
            'HeroSection',
            'FeatureGrid',
            'TestimonialCarousel',
            'LeadForm',
            'CTABanner',
            'Footer'
        ]
    elif page_type == 'blog':
        components = [
            'BlogHeader',
            'TableOfContents',
            'ContentBody',
            'AuthorBio',
            'RelatedPosts',
            'CTABanner'
        ]
    
    return components
```

### 4.2 OpenDesign API Integration

**Step 1: Call OpenDesign API**
```python
import requests

def call_opendesign(content: str, style: dict, components: list) -> dict:
    """Call OpenDesign API to generate components"""
    
    response = requests.post(
        'http://localhost:3000/api/v1/generate',
        json={
            'content': content,
            'style': style,
            'components': components,
            'framework': 'react-tailwind'
        },
        timeout=60
    )
    
    if response.status_code == 200:
        return response.json()
    else:
        raise Exception(f"OpenDesign API error: {response.text}")
```

**Step 2: Parse Generated Components**
```python
def parse_generated_components(api_response: dict) -> list:
    """Parse components from OpenDesign response"""
    
    components = []
    for comp in api_response.get('components', []):
        components.append({
            'name': comp['name'],
            'code': comp['code'],
            'dependencies': comp.get('dependencies', []),
            'props': comp.get('props', {})
        })
    
    return components
```

### 4.3 Content Integration Workflow

**Step 1: Inject Content into Components**
```python
def inject_content(component_code: str, content_data: dict) -> str:
    """Replace placeholders with actual content"""
    
    # Replace title
    component_code = component_code.replace(
        '{{title}}', 
        content_data['title']
    )
    
    # Replace subtitle
    component_code = component_code.replace(
        '{{subtitle}}', 
        content_data.get('metaDescription', '')
    )
    
    # Replace CTA text
    component_code = component_code.replace(
        '{{ctaText}}', 
        'Request Demo'
    )
    
    # Replace content body
    component_code = component_code.replace(
        '{{content}}', 
        content_data['content'][:500] + '...'  # Preview
    )
    
    return component_code
```

**Step 2: Apply Brand Colors**
```python
def apply_brand_colors(component_code: str, brand: dict) -> str:
    """Replace default colors with brand colors"""
    
    # Replace primary color
    component_code = component_code.replace(
        'bg-blue-900', 
        f'bg-[{brand["primaryColor"]}]'
    )
    
    # Replace secondary color
    component_code = component_code.replace(
        'bg-yellow-500', 
        f'bg-[{brand["secondaryColor"]}]'
    )
    
    return component_code
```

**Step 3: Generate Page Layout**
```python
def generate_page_layout(components: list, content_data: dict) -> str:
    """Assemble components into complete page"""
    
    page_template = """
import {{ {imports} }} from "@/components";

export default function {pageName}() {{
  return (
    <div className="min-h-screen">
      {components}
    </div>
  );
}}
"""
    
    # Extract imports
    imports = ', '.join([c['name'] for c in components])
    
    # Assemble components
    components_jsx = '\n      '.join([
        f'<{c["name"]} {{...{c["name"]}Props}} />' 
        for c in components
    ])
    
    # Generate page
    page = page_template.format(
        imports=imports,
        pageName=content_data['slug'].replace('-', ' ').title().replace(' ', ''),
        components=components_jsx
    )
    
    return page
```

### 4.4 Gamma.app Integration

**Step 1: Generate Infographic Request**
```python
def create_infographic_request(content: str) -> dict:
    """Create Gamma.app infographic generation request"""
    
    # Extract key statistics
    stats = extract_statistics(content)
    
    return {
        'title': f"{content['title']} - Key Statistics",
        'content': ', '.join(stats),
        'format': 'presentation_16:9',
        'style': 'professional',
        'brandColors': [
            brand['primaryColor'],
            brand['secondaryColor']
        ]
    }
```

**Step 2: Call Gamma.app API**
```python
def call_gamma_app(infographic_data: dict) -> str:
    """Call Gamma.app API to generate infographic"""
    
    response = requests.post(
        'https://public-api.gamma.app/v1/generations',
        headers={
            'X-API-KEY': GAMMA_API_KEY,
            'Content-Type': 'application/json'
        },
        json=infographic_data,
        timeout=120
    )
    
    if response.status_code == 200:
        result = response.json()
        return result['generationId']
    else:
        raise Exception(f"Gamma.app API error: {response.text}")
```

---

## 5. Tools Required

### 5.1 OpenClaw Tools

| Tool | Permission | Purpose |
|------|------------|---------|
| `read` | Allow | Read content drafts, brand guidelines |
| `write` | Allow | Write generated components |
| `edit` | Allow | Edit and refine designs |
| `canvas` | Allow | Visual layout planning |
| `browser` | Allow | Browse design inspiration |
| `web_fetch` | Allow | Fetch design examples |
| `exec` | Allow | Run Python scripts for APIs |

### 5.2 External APIs

| API | Purpose | Free Tier | MVP Usage |
|-----|---------|-----------|-----------|
| **OpenDesign** | Component generation | Self-hosted (free) | Unlimited |
| **Gamma.app** | Infographic generation | Already have API key | As needed |

### 5.3 Python Dependencies

```txt
python-frontmatter     # Markdown parsing
requests               # HTTP requests for APIs
neo4j                  # Neo4j driver for brand guidelines
```

---

## 6. Configuration

### 6.1 Environment Variables

```bash
# OpenDesign
OPENDESIGN_URL=http://localhost:3000

# Gamma.app
GAMMA_API_KEY=sk-gamma-xxx

# Neo4j
NEO4J_URI=bolt://localhost:7687
NEO4J_USER=neo4j
NEO4J_PASSWORD=your-password

# OpenClaw
OPENCLAW_WORKSPACE=/root/.openclaw/workspace-designer-a
```

### 6.2 Model Configuration

```json
{
  "model": {
    "primary": "ollama-cloud/minimax-m3",
    "fallbacks": ["ollama-cloud/deepseek-v4-pro"],
    "timeoutSeconds": 600
  }
}
```

### 6.3 Tool Configuration

```json
{
  "tools": {
    "allow": [
      "read",
      "write",
      "edit",
      "canvas",
      "browser",
      "web_fetch",
      "exec"
    ],
    "deny": [
      "process",
      "cron"
    ]
  }
}
```

---

## 7. Testing

### 7.1 Unit Tests

**Test: Content Parsing**
```python
def test_content_parsing():
    content = parse_content('workspace-vertical-a/drafts/test-article.md')
    assert 'title' in content
    assert 'content' in content
    assert 'slug' in content
```

**Test: Component Generation**
```python
def test_component_generation():
    components = call_opendesign(
        content="Test content",
        style={'industry': 'professional'},
        components=['hero', 'features']
    )
    assert 'components' in components
    assert len(components['components']) >= 2
```

### 7.2 Integration Tests

**Test: Full Design Workflow**
```python
async def test_full_design_workflow():
    # 1. Spawn designer agent
    await sessions_spawn(
        agentId="designer-vertical-a",
        task="Design 3 landing pages",
        params={
            "contentFiles": ["workspace-vertical-a/drafts/*.md"],
            "brandGuidelines": {"primaryColor": "#1e3a8a"}
        }
    )
    
    # 2. Wait for completion (timeout: 90 minutes)
    await wait_for_completion(timeout=5400)
    
    # 3. Verify outputs
    pages_dir = "workspace-designer-a/pages"
    pages = glob(f"{pages_dir}/*.tsx")
    assert len(pages) >= 3
    
    # 4. Verify components generated
    components_dir = "workspace-designer-a/components"
    components = glob(f"{components_dir}/*.tsx")
    assert len(components) >= 5
    
    # 5. Verify Linear updated
    task = await linear.getIssue("MAR-127")
    assert task.stateId == "done"
```

### 7.3 Success Criteria

- ✅ All pages integrate content correctly
- ✅ Brand colors applied consistently
- ✅ Components are production-ready (no placeholders)
- ✅ Mobile-first responsive design
- ✅ Accessible (WCAG 2.1 AA)
- ✅ CTAs aligned with business objective
- ✅ Design completes within 90 minutes for 5 pages
- ✅ Linear task updated with summary

---

## 8. Error Handling

### 8.1 OpenDesign API Failures

**Scenario:** OpenDesign service unavailable

**Detection:**
```python
try:
    response = call_opendesign(content, style, components)
except requests.ConnectionError:
    logger.error("OpenDesign service unavailable")
    # Fall back to template library
    components = use_template_library(content, style)
```

**Recovery:**
1. Use pre-built component templates
2. Retry OpenDesign every 15 minutes
3. Notify human if >1 hour downtime

### 8.2 Content Integration Errors

**Scenario:** Content doesn't fit component structure

**Detection:**
```python
def validate_content_fit(component: str, content: dict) -> bool:
    # Check if content length is appropriate
    if len(content['content']) > 5000:
        return False
    
    # Check if required fields exist
    required = ['title', 'content', 'slug']
    return all(field in content for field in required)
```

**Recovery:**
1. Truncate or summarize content
2. Request writer agent to revise
3. Use alternative component layout

### 8.3 Gamma.app API Failures

**Scenario:** Gamma.app API rate limit or timeout

**Detection:**
```python
try:
    generation_id = call_gamma_app(infographic_data)
except requests.HTTPError as e:
    logger.error(f"Gamma.app API error: {e}")
    # Skip infographic, continue with design
    infographic_id = None
```

**Recovery:**
1. Skip infographic generation
2. Retry Gamma.app API every 30 minutes
3. Use placeholder image instead

---

## 9. Design Guidelines

### 9.1 Component Standards

**Code Quality:**
- TypeScript with proper types
- Tailwind CSS for styling
- Accessible (ARIA labels, keyboard navigation)
- Responsive (mobile-first)
- No hardcoded values (use props)

**Example Component:**
```tsx
interface HeroSectionProps {
  title: string;
  subtitle: string;
  ctaText: string;
  ctaLink: string;
  className?: string;
}

export function HeroSection({ 
  title, 
  subtitle, 
  ctaText, 
  ctaLink,
  className 
}: HeroSectionProps) {
  return (
    <section className={`py-20 ${className || ''}`}>
      {/* Accessible, responsive, typed */}
    </section>
  );
}
```

### 9.2 Brand Alignment

**Colors:**
- Primary: #1e3a8a (blue-900)
- Secondary: #f59e0b (amber-500)
- Accent: Use sparingly for CTAs

**Typography:**
- Headings: Bold, 2.5rem+ for H1
- Body: 1rem, line-height 1.6
- CTAs: Bold, uppercase

**Mood:**
- Professional
- Trustworthy
- Modern but not trendy

### 9.3 Conversion Optimization

**CTA Placement:**
- Above the fold (hero section)
- After key benefits
- At end of page
- Sticky header/footer on mobile

**CTA Design:**
- High contrast colors
- Clear action text ("Request Demo", not "Submit")
- Large touch targets (48x48px minimum)
- Multiple CTAs on long pages

---

## 10. Performance Metrics

| Metric | Target | Measurement |
|--------|--------|-------------|
| **Design Velocity** | 5 pages/90 min | Pages completed / Time |
| **Component Reuse** | 80%+ | Reused components / Total |
| **Content Integration** | 100% | Pages with content / Total |
| **Brand Compliance** | 100% | Pages with brand colors / Total |
| **Mobile Responsiveness** | 100% | Pages passing mobile test / Total |
| **Accessibility Score** | 95+ | Lighthouse accessibility / Total |
| **Design Duration** | <90 min for 5 pages | Start to completion time |

---

**Document End**

*Last updated: 2026-07-26*  
*Version: 1.0*  
*Next review: After Phase 4 implementation*
