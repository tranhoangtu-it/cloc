# Documentation Style Guide

## Overview

This style guide provides comprehensive guidelines for writing, maintaining, and using documentation in the cloc project. It ensures consistency, clarity, and usefulness across all documentation files.

## Table of Contents

1. [Documentation Structure](#documentation-structure)
2. [Writing Guidelines](#writing-guidelines)
3. [API Documentation Standards](#api-documentation-standards)
4. [Code Examples](#code-examples)
5. [Formatting and Style](#formatting-and-style)
6. [Maintenance Guidelines](#maintenance-guidelines)
7. [Review Process](#review-process)
8. [Templates](#templates)
9. [Tools and Automation](#tools-and-automation)
10. [Best Practices](#best-practices)

---

## Documentation Structure

### File Organization

```
docs/
├── API_DOCUMENTATION.md          # Complete API reference
├── COMPONENTS_DOCUMENTATION.md   # Component specifications
├── FUNCTION_REFERENCE.md         # Function documentation
├── DOCUMENTATION_STYLE_GUIDE.md  # This file
├── QUICK_START.md                # Getting started guide
├── EXAMPLES.md                   # Usage examples
├── TROUBLESHOOTING.md            # Common issues and solutions
└── CHANGELOG.md                  # Version history
```

### Documentation Types

#### 1. API Documentation
- **Purpose**: Complete reference for all public APIs
- **Audience**: Developers using the library
- **Format**: Detailed technical specifications
- **Update Frequency**: With each API change

#### 2. Component Documentation
- **Purpose**: Detailed component specifications
- **Audience**: Developers working with components
- **Format**: Technical reference with examples
- **Update Frequency**: With component changes

#### 3. Function Reference
- **Purpose**: Complete function documentation
- **Audience**: Developers using functions
- **Format**: Detailed function signatures and examples
- **Update Frequency**: With function changes

#### 4. User Guides
- **Purpose**: Step-by-step instructions
- **Audience**: End users and new developers
- **Format**: Tutorial style with examples
- **Update Frequency**: With feature additions

#### 5. Style Guides
- **Purpose**: Documentation standards
- **Audience**: Documentation contributors
- **Format**: Guidelines and templates
- **Update Frequency**: As standards evolve

---

## Writing Guidelines

### Voice and Tone

#### Use Active Voice
```markdown
✅ Good: "The function returns a promise"
❌ Bad: "A promise is returned by the function"
```

#### Be Concise and Clear
```markdown
✅ Good: "Analyzes code complexity"
❌ Bad: "This function is responsible for the analysis of code complexity metrics"
```

#### Use Present Tense
```markdown
✅ Good: "The method calculates the result"
❌ Bad: "The method will calculate the result"
```

### Language Standards

#### Technical Terms
- Use consistent terminology throughout
- Define acronyms on first use
- Maintain a glossary of project-specific terms

#### Code References
- Use backticks for inline code: `functionName()`
- Use code blocks for multi-line code
- Reference classes, methods, and variables consistently

#### Examples
```markdown
Use `countLines()` to analyze a file:

```javascript
const result = await countLines('./src/app.js');
console.log(result.total);
```
```

---

## API Documentation Standards

### Function Documentation Format

```javascript
/**
 * Brief description of what the function does
 * 
 * @param {type} paramName - Description of parameter
 * @param {type} [optionalParam=default] - Description of optional parameter
 * @returns {type} Description of return value
 * @throws {ErrorType} Description of when this error is thrown
 * @example
 * // Example usage
 * const result = await functionName(param1, param2);
 * console.log(result);
 * @since 1.0.0
 * @deprecated Use newFunction() instead
 */
async function functionName(paramName, optionalParam = defaultValue) {
  // Implementation
}
```

### Parameter Documentation

#### Parameter Table Format
```markdown
| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `filePath` | string | Yes | - | Path to the file to analyze |
| `options` | object | No | `{}` | Configuration options |
| `options.recursive` | boolean | No | `true` | Whether to recurse into subdirectories |
```

#### Type Definitions
- Use TypeScript-style type annotations
- Document union types: `string | number`
- Document array types: `Array<string>` or `string[]`
- Document object shapes with detailed structures

### Return Value Documentation

#### Simple Returns
```markdown
#### Returns
- **Type**: `Promise<string>`
- **Description**: Promise that resolves to the file content
```

#### Complex Returns
```markdown
#### Returns
- **Type**: `Promise<AnalysisResult>`
- **Description**: Promise that resolves to analysis results

#### AnalysisResult Object Structure
```javascript
{
  file: string,           // File path
  language: string,       // Detected language
  lines: {
    total: number,        // Total lines
    code: number,         // Code lines
    comments: number,     // Comment lines
    blank: number         // Blank lines
  }
}
```
```

### Error Documentation

#### Error List Format
```markdown
#### Errors
- `FileNotFoundError`: File does not exist
- `PermissionError`: Insufficient permissions to read file
- `UnsupportedFileTypeError`: File type not supported
```

#### Error Handling Examples
```javascript
try {
  const result = await analyzeFile('./file.js');
} catch (error) {
  if (error instanceof FileNotFoundError) {
    console.error('File not found');
  } else {
    console.error('Unexpected error:', error.message);
  }
}
```

---

## Code Examples

### Example Structure

#### 1. Basic Usage
```javascript
// Simple, minimal example
const result = await countLines('./src/app.js');
console.log(result.total);
```

#### 2. Advanced Usage
```javascript
// Complex example with options
const result = await countLines('./src/app.js', {
  includeComments: true,
  includeBlankLines: false,
  fileType: 'javascript'
});

console.log(`Total lines: ${result.total}`);
console.log(`Code lines: ${result.code}`);
```

#### 3. Error Handling
```javascript
// Example with proper error handling
try {
  const result = await countLines('./src/app.js');
  console.log(result);
} catch (error) {
  console.error('Analysis failed:', error.message);
}
```

### Code Example Guidelines

#### Best Practices
1. **Complete Examples**: Include all necessary imports and setup
2. **Realistic Examples**: Use realistic data and scenarios
3. **Error Handling**: Show proper error handling patterns
4. **Comments**: Add explanatory comments for complex logic
5. **Output**: Show expected output when helpful

#### Example Template
```javascript
// Import required modules
import { functionName } from 'cloc';

// Setup (if needed)
const options = {
  option1: 'value1',
  option2: 'value2'
};

// Main example
try {
  const result = await functionName(input, options);
  console.log(result);
  // Output: { property: 'value' }
} catch (error) {
  console.error('Error:', error.message);
}
```

---

## Formatting and Style

### Markdown Standards

#### Headers
- Use descriptive headers
- Follow hierarchical structure (H1 > H2 > H3)
- Use sentence case for headers

#### Lists
- Use consistent bullet points
- Use numbered lists for sequential steps
- Indent sub-items properly

#### Tables
- Include headers for all tables
- Align columns consistently
- Use pipes for clear separation

#### Code Blocks
- Specify language for syntax highlighting
- Use consistent indentation
- Include comments for clarity

### Typography

#### Emphasis
- Use **bold** for important terms
- Use *italic* for emphasis
- Use `code` for technical terms

#### Links
- Use descriptive link text
- Link to relevant sections and external resources
- Test all links regularly

#### Images
- Use alt text for accessibility
- Optimize image sizes
- Use descriptive filenames

---

## Maintenance Guidelines

### Update Process

#### 1. Version Control
- Create documentation branches for major changes
- Use meaningful commit messages
- Tag documentation versions

#### 2. Change Tracking
- Document changes in CHANGELOG.md
- Use semantic versioning for documentation
- Track breaking changes separately

#### 3. Review Schedule
- Review documentation monthly
- Update examples with new features
- Check for outdated information

### Consistency Checks

#### Regular Audits
1. **Link Validation**: Check all internal and external links
2. **Code Example Testing**: Verify all examples work
3. **Terminology Consistency**: Ensure consistent term usage
4. **Format Consistency**: Check formatting standards

#### Automated Checks
- Use linters for markdown formatting
- Implement automated link checking
- Test code examples in CI/CD pipeline

---

## Review Process

### Review Checklist

#### Content Review
- [ ] Information is accurate and up-to-date
- [ ] Examples work correctly
- [ ] Terminology is consistent
- [ ] Grammar and spelling are correct

#### Technical Review
- [ ] Code examples are tested
- [ ] API documentation matches implementation
- [ ] Error cases are documented
- [ ] Performance implications are noted

#### Style Review
- [ ] Follows style guide standards
- [ ] Formatting is consistent
- [ ] Links work correctly
- [ ] Images are optimized

### Approval Process

#### Documentation Changes
1. **Minor Updates**: Single reviewer approval
2. **Major Changes**: Two reviewer approval
3. **API Changes**: Technical lead approval
4. **Style Changes**: Documentation team approval

#### Review Timeline
- Minor updates: 1-2 business days
- Major changes: 3-5 business days
- Breaking changes: 1 week review period

---

## Templates

### Function Documentation Template

```markdown
### `functionName(parameter1, parameter2)`

Brief description of what the function does.

#### Signature
```javascript
async function functionName(parameter1, parameter2 = defaultValue)
```

#### Parameters
| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `parameter1` | string | Yes | - | Description of parameter |
| `parameter2` | object | No | `{}` | Description of optional parameter |

#### Returns
- **Type**: `Promise<ReturnType>`
- **Description**: Description of return value

#### Errors
- `ErrorType`: Description of when this error occurs

#### Example
```javascript
const result = await functionName('input', { option: 'value' });
console.log(result);
```
```

### Component Documentation Template

```markdown
### ComponentName

Brief description of the component.

#### Constructor
```javascript
const component = new ComponentName(options);
```

#### Options
| Option | Type | Default | Description |
|--------|------|---------|-------------|
| `option1` | boolean | `true` | Description of option |

#### Methods

##### `methodName(parameter)`
Description of method.

#### Events
- `eventName`: Description of when event is emitted

#### Example
```javascript
const component = new ComponentName({
  option1: true
});

component.on('eventName', (data) => {
  console.log(data);
});
```
```

### API Endpoint Template

```markdown
### POST /api/endpoint

Description of the endpoint.

#### Request
```json
{
  "parameter": "value"
}
```

#### Response
```json
{
  "result": "success",
  "data": {}
}
```

#### Error Responses
- `400`: Bad Request - Invalid parameters
- `404`: Not Found - Resource not found
- `500`: Internal Server Error - Server error

#### Example
```javascript
const response = await fetch('/api/endpoint', {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json'
  },
  body: JSON.stringify({
    parameter: 'value'
  })
});
```
```

---

## Tools and Automation

### Documentation Tools

#### Markdown Processors
- **Recommended**: Markdown-it, Remark
- **Features**: Syntax highlighting, table of contents generation
- **Plugins**: Link validation, spell checking

#### Documentation Generators
- **JSDoc**: For JavaScript documentation
- **TypeDoc**: For TypeScript documentation
- **Sphinx**: For Python documentation

#### Linting Tools
- **markdownlint**: Markdown formatting
- **textlint**: Writing style and grammar
- **alex**: Inclusive language checking

### Automation Scripts

#### Link Checker
```bash
#!/bin/bash
# Check all markdown files for broken links
find docs -name "*.md" -exec markdown-link-check {} \;
```

#### Example Testing
```bash
#!/bin/bash
# Extract and test all code examples
extract-examples docs/ | test-examples
```

#### Documentation Build
```bash
#!/bin/bash
# Build documentation site
npm run docs:build
npm run docs:test
npm run docs:deploy
```

---

## Best Practices

### Writing Principles

#### 1. User-Centric Approach
- Write for the user's needs
- Provide context and motivation
- Include troubleshooting information

#### 2. Comprehensive Coverage
- Document all public APIs
- Include edge cases and limitations
- Provide migration guides for breaking changes

#### 3. Practical Examples
- Use realistic scenarios
- Show complete working examples
- Include common use cases

### Documentation Architecture

#### 1. Hierarchical Structure
- Organize by user journey
- Use clear navigation
- Provide search functionality

#### 2. Cross-References
- Link related sections
- Provide context for complex topics
- Use consistent terminology

#### 3. Versioning Strategy
- Maintain version-specific documentation
- Archive old versions
- Provide migration guides

### Quality Assurance

#### 1. Testing
- Test all code examples
- Validate API responses
- Check cross-platform compatibility

#### 2. Review Process
- Peer review for accuracy
- User testing for clarity
- Regular audits for completeness

#### 3. Feedback Loop
- Collect user feedback
- Monitor usage analytics
- Iterate based on insights

---

## Conclusion

This style guide ensures consistent, high-quality documentation that serves users effectively. By following these guidelines, we maintain documentation that is:

- **Accurate**: Reflects current implementation
- **Complete**: Covers all use cases
- **Accessible**: Easy to find and understand
- **Maintainable**: Can be updated efficiently
- **Useful**: Helps users achieve their goals

Remember that documentation is a living resource that should evolve with the project and user needs.

---

## Quick Reference

### Common Formatting
- Function names: `functionName()`
- File paths: `./src/file.js`
- Code blocks: Use language-specific syntax highlighting
- Links: `[Link Text](url)`
- Emphasis: **bold** for important, *italic* for emphasis

### Documentation Commands
```bash
# Generate documentation
npm run docs:generate

# Validate documentation
npm run docs:validate

# Test examples
npm run docs:test-examples

# Build documentation site
npm run docs:build
```

### Resources
- [Markdown Guide](https://www.markdownguide.org/)
- [JSDoc Documentation](https://jsdoc.app/)
- [Technical Writing Guidelines](https://developers.google.com/tech-writing)

---

*This style guide is maintained by the documentation team and updated regularly to reflect best practices and tool changes.*