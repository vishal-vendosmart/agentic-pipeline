# Integration Specification: OpenDesign

**Service:** OpenDesign API  
**Purpose:** Generate React/Tailwind components from content  
**Integration Type:** REST API  
**Cost:** Self-hosted (free, open-source)  

---

## 1. Overview

OpenDesign converts content and style preferences into production-ready React/Tailwind components. The Designer agent uses OpenDesign to generate landing pages, blog templates, and UI components.

---

## 2. Setup

### 2.1 Docker Installation

```bash
docker run -d \
  --name opendesign \
  -p 3000:3000 \
  -v opendesign-data:/app/data \
  ghcr.io/opendesign/opendesign:latest
```

### 2.2 Access

- **API endpoint:** http://localhost:3000
- **UI:** http://localhost:3000 (if enabled)

### 2.3 Health Check

```bash
curl http://localhost:3000/api/health
# Should return: {"status": "ok"}
```

---

## 3. API Endpoints

### 3.1 Generate Components

**Endpoint:** `POST /api/v1/generate`

**Request:**
```json
{
  "content": "AI Procurement Software landing page with hero, features, form, CTA",
  "style": {
    "industry": "professional",
    "colors": ["#1e3a8a", "#ffffff", "#f59e0b"],
    "mood": "trustworthy, modern"
  },
  "components": ["hero", "feature-grid", "lead-form", "cta-banner"],
  "framework": "react-tailwind"
}
```

**Response:**
```json
{
  "components": [
    {
      "name": "HeroSection",
      "code": "export function HeroSection(props) { ... }",
      "dependencies": ["@/components/ui/button"],
      "props": {
        "title": "string",
        "subtitle": "string",
        "ctaText": "string"
      }
    },
    {
      "name": "FeatureGrid",
      "code": "export function FeatureGrid(props) { ... }",
      "dependencies": ["@/components/ui/card"],
      "props": {
        "features": "array"
      }
    }
  ],
  "styles": "body { font-family: Inter; }",
  "layout": "page structure"
}
```

### 3.2 Get Component Library

**Endpoint:** `GET /api/v1/components`

**Response:**
```json
{
  "components": [
    {"name": "HeroSection", "category": "layout"},
    {"name": "FeatureGrid", "category": "content"},
    {"name": "LeadForm", "category": "form"},
    {"name": "CTABanner", "category": "conversion"}
  ]
}
```

---

## 4. Python Integration

### 4.1 Client Class

```python
import requests
from typing import List, Dict

class OpenDesignClient:
    def __init__(self, base_url: str = 'http://localhost:3000'):
        self.base_url = base_url
    
    def generate(self, content: str, style: Dict, components: List[str]) -> Dict:
        """Generate components from content"""
        
        response = requests.post(
            f'{self.base_url}/api/v1/generate',
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
    
    def get_components(self) -> List[Dict]:
        """Get available component library"""
        
        response = requests.get(f'{self.base_url}/api/v1/components')
        
        if response.status_code == 200:
            return response.json()['components']
        else:
            raise Exception(f"OpenDesign API error: {response.text}")
```

### 4.2 Usage Example

```python
# Initialize client
client = OpenDesignClient('http://localhost:3000')

# Generate components
result = client.generate(
    content="AI procurement landing page with hero, 3 features, lead form, CTA",
    style={
        'industry': 'professional',
        'colors': ['#1e3a8a', '#ffffff', '#f59e0b'],
        'mood': 'trustworthy'
    },
    components=['hero', 'feature-grid', 'lead-form', 'cta-banner']
)

# Parse components
for component in result['components']:
    print(f"Generated: {component['name']}")
    print(f"Dependencies: {component['dependencies']}")
    print(f"Props: {component['props']}")
```

---

## 5. Component Templates

### 5.1 Hero Section

**Input:**
```json
{
  "content": "Reduce procurement costs by 30% with AI",
  "style": {
    "primaryColor": "#1e3a8a",
    "secondaryColor": "#f59e0b"
  }
}
```

**Output:**
```tsx
export function HeroSection({ title, subtitle, ctaText }) {
  return (
    <section className="py-20 bg-gradient-to-r from-blue-900 to-blue-800">
      <div className="container mx-auto px-4">
        <h1 className="text-5xl font-bold text-white mb-6">
          {title}
        </h1>
        <p className="text-xl text-blue-100 mb-8">
          {subtitle}
        </p>
        <Button size="lg" className="bg-white text-blue-900">
          {ctaText}
        </Button>
      </div>
    </section>
  );
}
```

### 5.2 Feature Grid

**Input:**
```json
{
  "content": "30% cost reduction, 80% time savings, real-time analytics",
  "style": {
    "columns": 3
  }
}
```

**Output:**
```tsx
export function FeatureGrid({ features }) {
  return (
    <section className="py-16">
      <div className="container mx-auto px-4">
        <div className="grid md:grid-cols-3 gap-8">
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
```

---

## 6. Customization

### 6.1 Brand Colors

```python
def apply_brand_colors(component_code: str, brand_colors: Dict) -> str:
    """Replace default colors with brand colors"""
    
    replacements = {
        'bg-blue-900': f'bg-[{brand_colors["primary"]}]',
        'bg-yellow-500': f'bg-[{brand_colors["secondary"]}]',
        'text-blue-900': f'text-[{brand_colors["primary"]}]'
    }
    
    for default, brand in replacements.items():
        component_code = component_code.replace(default, brand)
    
    return component_code
```

### 6.2 Content Integration

```python
def inject_content(component_code: str, content: Dict) -> str:
    """Replace placeholders with actual content"""
    
    replacements = {
        '{{title}}': content['title'],
        '{{subtitle}}': content['subtitle'],
        '{{ctaText}}': content['ctaText'],
        '{{content}}': content['body']
    }
    
    for placeholder, value in replacements.items():
        component_code = component_code.replace(placeholder, value)
    
    return component_code
```

---

## 7. Error Handling

### 7.1 API Failures

```python
try:
    result = client.generate(content, style, components)
except requests.ConnectionError:
    logger.error("OpenDesign service unavailable")
    # Fall back to template library
    components = use_template_library(content, style)
except requests.Timeout:
    logger.error("OpenDesign API timeout")
    # Retry with exponential backoff
    time.sleep(60)
    result = client.generate(content, style, components)
```

### 7.2 Invalid Input

```python
def validate_input(content: str, style: Dict, components: List[str]) -> bool:
    """Validate input before sending to API"""
    
    if not content or len(content) < 10:
        return False
    
    if not style or 'colors' not in style:
        return False
    
    if not components or len(components) == 0:
        return False
    
    return True
```

---

## 8. Testing

### 8.1 Unit Tests

```python
def test_generate_components():
    client = OpenDesignClient()
    
    result = client.generate(
        content="Test landing page",
        style={'colors': ['#000000']},
        components=['hero']
    )
    
    assert 'components' in result
    assert len(result['components']) > 0
    assert result['components'][0]['name'] == 'HeroSection'
```

### 8.2 Integration Tests

```python
def test_full_workflow():
    client = OpenDesignClient()
    
    # 1. Generate components
    result = client.generate(
        content="AI procurement landing page",
        style={
            'industry': 'professional',
            'colors': ['#1e3a8a', '#f59e0b']
        },
        components=['hero', 'feature-grid', 'lead-form']
    )
    
    # 2. Verify components generated
    assert len(result['components']) >= 3
    
    # 3. Verify code is valid TypeScript
    for component in result['components']:
        assert 'export function' in component['code']
        assert 'props' in component
```

---

## 9. Cost

| Component | Cost | Notes |
|-----------|------|-------|
| **OpenDesign** | $0 | Open-source, self-hosted |
| **Docker** | $0 | Included in Hetzner server |
| **Storage** | $0 | Included |

**Total Monthly Cost:** $0

---

**Document End**

*Last updated: 2026-07-26*  
*Version: 1.0*
