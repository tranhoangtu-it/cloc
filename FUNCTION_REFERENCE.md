# Function Reference Guide

## Overview

This document provides comprehensive documentation for all public functions in the cloc project. Each function is documented with its signature, parameters, return values, error handling, and usage examples.

## Table of Contents

1. [Core Functions](#core-functions)
2. [Analysis Functions](#analysis-functions)
3. [File System Functions](#file-system-functions)
4. [Language Detection Functions](#language-detection-functions)
5. [Utility Functions](#utility-functions)
6. [Configuration Functions](#configuration-functions)
7. [Report Generation Functions](#report-generation-functions)
8. [Error Handling Functions](#error-handling-functions)
9. [Testing Functions](#testing-functions)
10. [Function Guidelines](#function-guidelines)

---

## Core Functions

### `countLines(filePath, options)`

Counts the lines of code in a file with detailed analysis.

#### Signature
```javascript
async function countLines(filePath, options = {})
```

#### Parameters
| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `filePath` | string | Yes | - | Path to the file to analyze |
| `options` | object | No | `{}` | Configuration options |
| `options.includeComments` | boolean | No | `false` | Whether to include comment lines in the count |
| `options.includeBlankLines` | boolean | No | `false` | Whether to include blank lines in the count |
| `options.fileType` | string | No | `null` | Override automatic file type detection |
| `options.encoding` | string | No | `'utf8'` | File encoding |

#### Returns
- **Type**: `Promise<LineCount>`
- **Description**: Promise that resolves to a line count object

#### LineCount Object Structure
```javascript
{
  file: string,           // File path
  language: string,       // Detected language
  total: number,          // Total lines
  code: number,           // Lines of code
  comments: number,       // Comment lines
  blank: number,          // Blank lines
  size: number,           // File size in bytes
  complexity: number      // Cyclomatic complexity
}
```

#### Errors
- `FileNotFoundError`: File does not exist
- `PermissionError`: Insufficient permissions to read file
- `UnsupportedFileTypeError`: File type not supported
- `InvalidEncodingError`: Invalid file encoding

#### Example
```javascript
// Basic usage
const lineCount = await countLines('./src/index.js');
console.log(`Total lines: ${lineCount.total}`);

// With options
const detailedCount = await countLines('./src/app.js', {
  includeComments: true,
  includeBlankLines: true,
  fileType: 'javascript'
});

console.log(detailedCount);
// Output: {
//   file: './src/app.js',
//   language: 'JavaScript',
//   total: 150,
//   code: 120,
//   comments: 20,
//   blank: 10,
//   size: 4096,
//   complexity: 15
// }
```

---

### `analyzeFile(filePath, options)`

Performs comprehensive analysis of a single file.

#### Signature
```javascript
async function analyzeFile(filePath, options = {})
```

#### Parameters
| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `filePath` | string | Yes | - | Path to the file to analyze |
| `options` | object | No | `{}` | Analysis options |
| `options.metrics` | boolean | No | `true` | Calculate code metrics |
| `options.complexity` | boolean | No | `true` | Calculate complexity metrics |
| `options.maintainability` | boolean | No | `true` | Calculate maintainability index |
| `options.duplicates` | boolean | No | `false` | Detect code duplicates |

#### Returns
- **Type**: `Promise<FileAnalysis>`
- **Description**: Promise that resolves to a comprehensive file analysis

#### FileAnalysis Object Structure
```javascript
{
  file: string,
  language: string,
  size: number,
  lines: {
    total: number,
    code: number,
    comments: number,
    blank: number
  },
  metrics: {
    cyclomatic: number,
    cognitive: number,
    halstead: {
      difficulty: number,
      effort: number,
      volume: number
    }
  },
  maintainability: {
    index: number,
    rank: string
  },
  duplicates: Array<DuplicateBlock>
}
```

#### Example
```javascript
const analysis = await analyzeFile('./src/utils.js', {
  metrics: true,
  complexity: true,
  maintainability: true
});

console.log(`Maintainability: ${analysis.maintainability.rank}`);
console.log(`Complexity: ${analysis.metrics.cyclomatic}`);
```

---

### `analyzeDirectory(directoryPath, options)`

Recursively analyzes all files in a directory.

#### Signature
```javascript
async function analyzeDirectory(directoryPath, options = {})
```

#### Parameters
| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `directoryPath` | string | Yes | - | Path to the directory to analyze |
| `options` | object | No | `{}` | Analysis options |
| `options.recursive` | boolean | No | `true` | Analyze subdirectories |
| `options.maxDepth` | number | No | `Infinity` | Maximum directory depth |
| `options.exclude` | array | No | `[]` | Patterns to exclude |
| `options.include` | array | No | `[]` | Patterns to include |
| `options.parallel` | boolean | No | `true` | Parallel processing |
| `options.maxConcurrency` | number | No | `4` | Maximum concurrent operations |

#### Returns
- **Type**: `Promise<DirectoryAnalysis>`
- **Description**: Promise that resolves to directory analysis results

#### DirectoryAnalysis Object Structure
```javascript
{
  directory: string,
  totalFiles: number,
  totalSize: number,
  totalLines: number,
  languages: {
    [language]: {
      files: number,
      lines: number,
      size: number
    }
  },
  fileTypes: {
    [extension]: number
  },
  summary: {
    avgComplexity: number,
    avgMaintainability: number,
    codeToCommentRatio: number
  },
  files: Array<FileAnalysis>
}
```

#### Example
```javascript
const analysis = await analyzeDirectory('./src', {
  recursive: true,
  maxDepth: 3,
  exclude: ['*.test.js', 'node_modules/**'],
  parallel: true
});

console.log(`Total files: ${analysis.totalFiles}`);
console.log(`Languages: ${Object.keys(analysis.languages).join(', ')}`);
```

---

## Analysis Functions

### `calculateComplexity(code, language)`

Calculates cyclomatic complexity for code.

#### Signature
```javascript
function calculateComplexity(code, language)
```

#### Parameters
| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `code` | string | Yes | - | Source code to analyze |
| `language` | string | Yes | - | Programming language |

#### Returns
- **Type**: `ComplexityMetrics`
- **Description**: Object containing complexity metrics

#### ComplexityMetrics Object Structure
```javascript
{
  cyclomatic: number,      // Cyclomatic complexity
  cognitive: number,       // Cognitive complexity
  essential: number,       // Essential complexity
  functions: Array<{
    name: string,
    complexity: number,
    startLine: number,
    endLine: number
  }>
}
```

#### Example
```javascript
const code = `
function fibonacci(n) {
  if (n <= 1) return n;
  return fibonacci(n - 1) + fibonacci(n - 2);
}
`;

const complexity = calculateComplexity(code, 'javascript');
console.log(`Cyclomatic complexity: ${complexity.cyclomatic}`);
// Output: Cyclomatic complexity: 2
```

---

### `calculateMaintainability(analysis)`

Calculates maintainability index based on code analysis.

#### Signature
```javascript
function calculateMaintainability(analysis)
```

#### Parameters
| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `analysis` | object | Yes | - | File analysis object |

#### Returns
- **Type**: `MaintainabilityIndex`
- **Description**: Maintainability metrics

#### MaintainabilityIndex Object Structure
```javascript
{
  index: number,           // Maintainability index (0-100)
  rank: string,            // Rank (A, B, C, D, F)
  factors: {
    complexity: number,
    volume: number,
    linesOfCode: number,
    commentRatio: number
  }
}
```

#### Example
```javascript
const fileAnalysis = await analyzeFile('./src/module.js');
const maintainability = calculateMaintainability(fileAnalysis);

console.log(`Maintainability: ${maintainability.index} (${maintainability.rank})`);
// Output: Maintainability: 85 (A)
```

---

## File System Functions

### `scanFiles(directoryPath, options)`

Scans directory for files matching specified criteria.

#### Signature
```javascript
async function scanFiles(directoryPath, options = {})
```

#### Parameters
| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `directoryPath` | string | Yes | - | Directory to scan |
| `options` | object | No | `{}` | Scanning options |
| `options.extensions` | array | No | `[]` | File extensions to include |
| `options.exclude` | array | No | `[]` | Patterns to exclude |
| `options.recursive` | boolean | No | `true` | Scan subdirectories |
| `options.followSymlinks` | boolean | No | `false` | Follow symbolic links |

#### Returns
- **Type**: `Promise<Array<string>>`
- **Description**: Array of file paths

#### Example
```javascript
const files = await scanFiles('./src', {
  extensions: ['.js', '.jsx', '.ts', '.tsx'],
  exclude: ['*.test.js', '*.spec.js'],
  recursive: true
});

console.log(`Found ${files.length} files`);
```

---

### `readFileContent(filePath, encoding)`

Reads and returns file content with error handling.

#### Signature
```javascript
async function readFileContent(filePath, encoding = 'utf8')
```

#### Parameters
| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `filePath` | string | Yes | - | Path to file |
| `encoding` | string | No | `'utf8'` | File encoding |

#### Returns
- **Type**: `Promise<string>`
- **Description**: File content as string

#### Errors
- `FileNotFoundError`: File does not exist
- `PermissionError`: Insufficient permissions
- `EncodingError`: Invalid encoding

#### Example
```javascript
try {
  const content = await readFileContent('./config.json');
  const config = JSON.parse(content);
} catch (error) {
  console.error('Failed to read config:', error.message);
}
```

---

## Language Detection Functions

### `detectLanguage(filePath)`

Detects the programming language of a file.

#### Signature
```javascript
function detectLanguage(filePath)
```

#### Parameters
| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `filePath` | string | Yes | - | Path to file |

#### Returns
- **Type**: `LanguageInfo`
- **Description**: Language information object

#### LanguageInfo Object Structure
```javascript
{
  name: string,            // Language name
  extension: string,       // File extension
  confidence: number,      // Detection confidence (0-1)
  aliases: Array<string>,  // Alternative names
  commentStyle: string     // Comment style
}
```

#### Example
```javascript
const language = detectLanguage('./script.py');
console.log(language.name); // 'Python'
console.log(language.confidence); // 0.95
```

---

### `getSupportedLanguages()`

Returns list of all supported programming languages.

#### Signature
```javascript
function getSupportedLanguages()
```

#### Parameters
None

#### Returns
- **Type**: `Array<LanguageDefinition>`
- **Description**: Array of supported languages

#### LanguageDefinition Object Structure
```javascript
{
  name: string,
  extensions: Array<string>,
  commentPatterns: Array<RegExp>,
  stringPatterns: Array<RegExp>,
  keywords: Array<string>,
  aliases: Array<string>
}
```

#### Example
```javascript
const languages = getSupportedLanguages();
console.log(`Supported languages: ${languages.length}`);

const jsLang = languages.find(lang => lang.name === 'JavaScript');
console.log(`JavaScript extensions: ${jsLang.extensions.join(', ')}`);
```

---

### `addLanguageDefinition(definition)`

Adds a new language definition to the detector.

#### Signature
```javascript
function addLanguageDefinition(definition)
```

#### Parameters
| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `definition` | object | Yes | - | Language definition |

#### Returns
- **Type**: `boolean`
- **Description**: True if successfully added

#### Example
```javascript
const customLanguage = {
  name: 'CustomLang',
  extensions: ['.custom'],
  commentPatterns: [/^#.*$/gm],
  stringPatterns: [/"[^"]*"/gm],
  keywords: ['func', 'var', 'if', 'else']
};

const added = addLanguageDefinition(customLanguage);
console.log(`Language added: ${added}`);
```

---

## Utility Functions

### `formatBytes(bytes, decimals)`

Formats byte count into human-readable string.

#### Signature
```javascript
function formatBytes(bytes, decimals = 2)
```

#### Parameters
| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `bytes` | number | Yes | - | Number of bytes |
| `decimals` | number | No | `2` | Decimal places |

#### Returns
- **Type**: `string`
- **Description**: Formatted byte string

#### Example
```javascript
console.log(formatBytes(1024)); // '1.00 KB'
console.log(formatBytes(1048576)); // '1.00 MB'
console.log(formatBytes(1073741824, 1)); // '1.0 GB'
```

---

### `formatDuration(milliseconds)`

Formats duration into human-readable string.

#### Signature
```javascript
function formatDuration(milliseconds)
```

#### Parameters
| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `milliseconds` | number | Yes | - | Duration in milliseconds |

#### Returns
- **Type**: `string`
- **Description**: Formatted duration string

#### Example
```javascript
console.log(formatDuration(1000)); // '1.00s'
console.log(formatDuration(65000)); // '1m 5s'
console.log(formatDuration(3661000)); // '1h 1m 1s'
```

---

### `createHash(input)`

Creates SHA-256 hash of input string.

#### Signature
```javascript
function createHash(input)
```

#### Parameters
| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `input` | string | Yes | - | Input string to hash |

#### Returns
- **Type**: `string`
- **Description**: Hexadecimal hash string

#### Example
```javascript
const hash = createHash('Hello, World!');
console.log(hash); // 'dffd6021bb2bd5b0af676290809ec3a53191dd81c7f70a4b28688a362182986f'
```

---

### `debounce(func, delay)`

Creates a debounced version of a function.

#### Signature
```javascript
function debounce(func, delay)
```

#### Parameters
| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `func` | function | Yes | - | Function to debounce |
| `delay` | number | Yes | - | Delay in milliseconds |

#### Returns
- **Type**: `function`
- **Description**: Debounced function

#### Example
```javascript
const debouncedSave = debounce(async (data) => {
  await saveToFile(data);
}, 300);

// Will only save after 300ms of inactivity
debouncedSave(data1);
debouncedSave(data2);
debouncedSave(data3); // Only this call will execute
```

---

## Configuration Functions

### `loadConfig(configPath)`

Loads configuration from file.

#### Signature
```javascript
async function loadConfig(configPath)
```

#### Parameters
| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `configPath` | string | No | `'./cloc.config.js'` | Path to configuration file |

#### Returns
- **Type**: `Promise<Configuration>`
- **Description**: Configuration object

#### Configuration Object Structure
```javascript
{
  exclude: Array<string>,
  include: Array<string>,
  languages: Object,
  output: {
    format: string,
    file: string,
    includeDetails: boolean
  },
  analysis: {
    complexity: boolean,
    maintainability: boolean,
    duplicates: boolean
  }
}
```

#### Example
```javascript
const config = await loadConfig('./my-config.js');
console.log(`Output format: ${config.output.format}`);
```

---

### `validateConfig(config)`

Validates configuration object against schema.

#### Signature
```javascript
function validateConfig(config)
```

#### Parameters
| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `config` | object | Yes | - | Configuration to validate |

#### Returns
- **Type**: `ValidationResult`
- **Description**: Validation result object

#### ValidationResult Object Structure
```javascript
{
  valid: boolean,
  errors: Array<{
    field: string,
    message: string,
    value: any
  }>
}
```

#### Example
```javascript
const result = validateConfig({
  exclude: ['*.test.js'],
  output: { format: 'json' }
});

if (!result.valid) {
  console.error('Configuration errors:', result.errors);
}
```

---

### `mergeConfigs(defaultConfig, userConfig)`

Merges user configuration with defaults.

#### Signature
```javascript
function mergeConfigs(defaultConfig, userConfig)
```

#### Parameters
| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `defaultConfig` | object | Yes | - | Default configuration |
| `userConfig` | object | Yes | - | User configuration |

#### Returns
- **Type**: `object`
- **Description**: Merged configuration object

#### Example
```javascript
const defaults = {
  recursive: true,
  exclude: [],
  output: { format: 'json' }
};

const userConfig = {
  exclude: ['*.test.js'],
  output: { format: 'html' }
};

const merged = mergeConfigs(defaults, userConfig);
console.log(merged.output.format); // 'html'
```

---

## Report Generation Functions

### `generateReport(data, options)`

Generates a report from analysis data.

#### Signature
```javascript
async function generateReport(data, options = {})
```

#### Parameters
| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `data` | object | Yes | - | Analysis data |
| `options` | object | No | `{}` | Report options |
| `options.format` | string | No | `'json'` | Output format |
| `options.template` | string | No | `'default'` | Template name |
| `options.outputPath` | string | No | `'./'` | Output directory |
| `options.filename` | string | No | `null` | Output filename |

#### Returns
- **Type**: `Promise<ReportResult>`
- **Description**: Report generation result

#### ReportResult Object Structure
```javascript
{
  success: boolean,
  format: string,
  file: string,
  size: number,
  generatedAt: Date
}
```

#### Example
```javascript
const report = await generateReport(analysisData, {
  format: 'html',
  template: 'detailed',
  outputPath: './reports',
  filename: 'project-analysis.html'
});

console.log(`Report generated: ${report.file}`);
```

---

### `exportToCSV(data, options)`

Exports analysis data to CSV format.

#### Signature
```javascript
async function exportToCSV(data, options = {})
```

#### Parameters
| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `data` | object | Yes | - | Analysis data |
| `options` | object | No | `{}` | Export options |
| `options.filename` | string | No | `'analysis.csv'` | Output filename |
| `options.delimiter` | string | No | `','` | CSV delimiter |
| `options.includeHeaders` | boolean | No | `true` | Include column headers |

#### Returns
- **Type**: `Promise<string>`
- **Description**: CSV content as string

#### Example
```javascript
const csvContent = await exportToCSV(analysisData, {
  filename: 'code-analysis.csv',
  delimiter: ';',
  includeHeaders: true
});

console.log('CSV exported successfully');
```

---

### `exportToJSON(data, options)`

Exports analysis data to JSON format.

#### Signature
```javascript
async function exportToJSON(data, options = {})
```

#### Parameters
| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `data` | object | Yes | - | Analysis data |
| `options` | object | No | `{}` | Export options |
| `options.filename` | string | No | `'analysis.json'` | Output filename |
| `options.pretty` | boolean | No | `true` | Pretty print JSON |
| `options.includeMetadata` | boolean | No | `true` | Include metadata |

#### Returns
- **Type**: `Promise<string>`
- **Description**: JSON content as string

#### Example
```javascript
const jsonContent = await exportToJSON(analysisData, {
  filename: 'detailed-analysis.json',
  pretty: true,
  includeMetadata: true
});

console.log('JSON exported successfully');
```

---

## Error Handling Functions

### `handleError(error, context)`

Centralized error handling function.

#### Signature
```javascript
function handleError(error, context = {})
```

#### Parameters
| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `error` | Error | Yes | - | Error object |
| `context` | object | No | `{}` | Additional context |

#### Returns
- **Type**: `ErrorInfo`
- **Description**: Processed error information

#### ErrorInfo Object Structure
```javascript
{
  type: string,
  message: string,
  stack: string,
  context: object,
  suggestions: Array<string>,
  recoverable: boolean
}
```

#### Example
```javascript
try {
  await analyzeFile('./nonexistent-file.js');
} catch (error) {
  const errorInfo = handleError(error, {
    operation: 'file-analysis',
    file: './nonexistent-file.js'
  });
  
  console.error(`Error: ${errorInfo.message}`);
  console.log(`Suggestions: ${errorInfo.suggestions.join(', ')}`);
}
```

---

### `createError(type, message, cause)`

Creates a custom error with type and cause.

#### Signature
```javascript
function createError(type, message, cause = null)
```

#### Parameters
| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `type` | string | Yes | - | Error type |
| `message` | string | Yes | - | Error message |
| `cause` | Error | No | `null` | Underlying cause |

#### Returns
- **Type**: `CustomError`
- **Description**: Custom error object

#### Example
```javascript
const error = createError('VALIDATION_ERROR', 'Invalid configuration', originalError);
throw error;
```

---

## Testing Functions

### `runTests(pattern, options)`

Runs tests matching the specified pattern.

#### Signature
```javascript
async function runTests(pattern, options = {})
```

#### Parameters
| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `pattern` | string | Yes | - | Test file pattern |
| `options` | object | No | `{}` | Test options |
| `options.timeout` | number | No | `5000` | Test timeout |
| `options.parallel` | boolean | No | `true` | Run tests in parallel |
| `options.reporter` | string | No | `'spec'` | Test reporter |

#### Returns
- **Type**: `Promise<TestResults>`
- **Description**: Test execution results

#### TestResults Object Structure
```javascript
{
  total: number,
  passed: number,
  failed: number,
  skipped: number,
  duration: number,
  tests: Array<{
    name: string,
    status: string,
    duration: number,
    error: string
  }>
}
```

#### Example
```javascript
const results = await runTests('**/*.test.js', {
  timeout: 10000,
  parallel: false,
  reporter: 'json'
});

console.log(`Tests: ${results.passed}/${results.total} passed`);
```

---

### `benchmark(func, iterations)`

Benchmarks a function's performance.

#### Signature
```javascript
async function benchmark(func, iterations = 100)
```

#### Parameters
| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `func` | function | Yes | - | Function to benchmark |
| `iterations` | number | No | `100` | Number of iterations |

#### Returns
- **Type**: `Promise<BenchmarkResult>`
- **Description**: Benchmark results

#### BenchmarkResult Object Structure
```javascript
{
  iterations: number,
  totalTime: number,
  averageTime: number,
  minTime: number,
  maxTime: number,
  opsPerSecond: number
}
```

#### Example
```javascript
const result = await benchmark(async () => {
  await analyzeFile('./test-file.js');
}, 50);

console.log(`Average time: ${result.averageTime}ms`);
console.log(`Operations per second: ${result.opsPerSecond}`);
```

---

## Function Guidelines

### Function Design Principles

1. **Single Responsibility**: Each function should have one clear purpose
2. **Pure Functions**: Prefer pure functions when possible
3. **Error Handling**: Always handle errors gracefully
4. **Documentation**: Document all public functions
5. **Testing**: Write tests for all public functions

### Function Documentation Template

```javascript
/**
 * Brief description of what the function does
 * @param {type} paramName - Description of parameter
 * @param {type} [optionalParam=default] - Description of optional parameter
 * @returns {type} Description of return value
 * @throws {ErrorType} Description of when this error is thrown
 * @example
 * // Example usage
 * const result = await functionName(param1, param2);
 * console.log(result);
 * @since 1.0.0
 */
async function functionName(paramName, optionalParam = defaultValue) {
  // Implementation
}
```

### Function Naming Conventions

- Use descriptive names: `calculateComplexity` instead of `calc`
- Use verbs for actions: `analyzeFile`, `generateReport`
- Use consistent prefixes: `get`, `set`, `is`, `has`, `can`
- Use camelCase for function names
- Use PascalCase for constructor functions

### Error Handling Best Practices

```javascript
async function exampleFunction(input) {
  try {
    // Validate input
    if (!input) {
      throw createError('INVALID_INPUT', 'Input is required');
    }
    
    // Perform operation
    const result = await performOperation(input);
    
    // Validate result
    if (!result) {
      throw createError('OPERATION_FAILED', 'Operation returned no result');
    }
    
    return result;
  } catch (error) {
    // Add context and re-throw
    throw createError('FUNCTION_ERROR', `Failed to process input: ${input}`, error);
  }
}
```

### Performance Considerations

- Use async/await for asynchronous operations
- Implement proper caching for expensive operations
- Use streaming for large files
- Consider parallel processing for independent operations
- Profile functions to identify bottlenecks

---

## Function Registry

### Available Functions by Category

#### Core Functions
- `countLines()`
- `analyzeFile()`
- `analyzeDirectory()`

#### Analysis Functions
- `calculateComplexity()`
- `calculateMaintainability()`
- `detectDuplicates()`

#### Language Detection
- `detectLanguage()`
- `getSupportedLanguages()`
- `addLanguageDefinition()`

#### File System
- `scanFiles()`
- `readFileContent()`
- `writeFileContent()`

#### Utilities
- `formatBytes()`
- `formatDuration()`
- `createHash()`
- `debounce()`

#### Configuration
- `loadConfig()`
- `validateConfig()`
- `mergeConfigs()`

#### Report Generation
- `generateReport()`
- `exportToCSV()`
- `exportToJSON()`

#### Error Handling
- `handleError()`
- `createError()`

#### Testing
- `runTests()`
- `benchmark()`

---

*This documentation is automatically generated from function source code. Last updated: $(date)*