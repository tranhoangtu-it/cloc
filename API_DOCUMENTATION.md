# API Documentation

## Overview

This document provides comprehensive documentation for all public APIs, functions, and components in the cloc project. It includes detailed descriptions, usage examples, and best practices.

## Table of Contents

1. [API Reference](#api-reference)
2. [Core Functions](#core-functions)
3. [Components](#components)
4. [Usage Examples](#usage-examples)
5. [Error Handling](#error-handling)
6. [Configuration](#configuration)
7. [Contributing](#contributing)

---

## API Reference

### Authentication

All API endpoints require authentication unless otherwise specified.

#### Authentication Headers
```
Authorization: Bearer <token>
Content-Type: application/json
```

### Base URL
```
https://api.cloc.example.com/v1
```

### Rate Limiting
- 1000 requests per hour for authenticated users
- 100 requests per hour for unauthenticated users

---

## Core Functions

### `countLines(filePath, options)`

Counts the lines of code in a given file.

#### Parameters
- `filePath` (string, required): Path to the file to analyze
- `options` (object, optional): Configuration options
  - `includeComments` (boolean, default: false): Whether to include comment lines in the count
  - `includeBlankLines` (boolean, default: false): Whether to include blank lines in the count
  - `fileType` (string, optional): Override file type detection

#### Returns
- `Promise<LineCount>`: Object containing line count information

#### Example
```javascript
const lineCount = await countLines('./src/index.js', {
  includeComments: true,
  includeBlankLines: false
});

console.log(lineCount);
// Output: { total: 150, code: 120, comments: 20, blank: 10 }
```

#### Error Handling
- Throws `FileNotFoundError` if file doesn't exist
- Throws `PermissionError` if file cannot be read
- Throws `UnsupportedFileTypeError` if file type is not supported

---

### `analyzeDirectory(directoryPath, options)`

Recursively analyzes all files in a directory and returns comprehensive statistics.

#### Parameters
- `directoryPath` (string, required): Path to the directory to analyze
- `options` (object, optional): Configuration options
  - `recursive` (boolean, default: true): Whether to analyze subdirectories
  - `exclude` (array, optional): Array of file patterns to exclude
  - `include` (array, optional): Array of file patterns to include
  - `maxDepth` (number, default: Infinity): Maximum directory depth to analyze

#### Returns
- `Promise<DirectoryAnalysis>`: Object containing comprehensive analysis

#### Example
```javascript
const analysis = await analyzeDirectory('./src', {
  recursive: true,
  exclude: ['*.test.js', 'node_modules/**'],
  maxDepth: 5
});

console.log(analysis);
// Output: {
//   totalFiles: 25,
//   totalLines: 5000,
//   languages: {
//     javascript: { files: 20, lines: 4000 },
//     typescript: { files: 5, lines: 1000 }
//   }
// }
```

---

### `getSupportedLanguages()`

Returns a list of all supported programming languages and file extensions.

#### Parameters
None

#### Returns
- `Array<LanguageInfo>`: Array of supported language objects

#### Example
```javascript
const languages = getSupportedLanguages();

console.log(languages);
// Output: [
//   { name: 'JavaScript', extensions: ['.js', '.jsx'], commentStyle: '//' },
//   { name: 'TypeScript', extensions: ['.ts', '.tsx'], commentStyle: '//' },
//   { name: 'Python', extensions: ['.py'], commentStyle: '#' }
// ]
```

---

## Components

### FileAnalyzer

A high-level component for analyzing individual files.

#### Constructor
```javascript
const analyzer = new FileAnalyzer(options);
```

#### Options
- `cacheResults` (boolean, default: true): Whether to cache analysis results
- `ignoreHidden` (boolean, default: true): Whether to ignore hidden files
- `customPatterns` (object, optional): Custom regex patterns for language detection

#### Methods

##### `analyze(filePath)`
Analyzes a single file and returns detailed metrics.

```javascript
const result = await analyzer.analyze('./src/main.js');
console.log(result);
// Output: {
//   file: './src/main.js',
//   language: 'JavaScript',
//   lines: { total: 150, code: 120, comments: 20, blank: 10 },
//   complexity: 15,
//   maintainabilityIndex: 85
// }
```

##### `getCache()`
Returns the current cache of analyzed files.

```javascript
const cache = analyzer.getCache();
console.log(cache);
// Output: Map containing cached results
```

##### `clearCache()`
Clears the analysis cache.

```javascript
analyzer.clearCache();
```

---

### ProjectAnalyzer

A comprehensive analyzer for entire projects.

#### Constructor
```javascript
const projectAnalyzer = new ProjectAnalyzer(projectPath, options);
```

#### Options
- `configFile` (string, optional): Path to configuration file
- `outputFormat` (string, default: 'json'): Output format ('json', 'csv', 'xml')
- `plugins` (array, optional): Array of plugin names to load

#### Methods

##### `run()`
Executes the full project analysis.

```javascript
const report = await projectAnalyzer.run();
console.log(report);
// Output: Comprehensive project analysis report
```

##### `generateReport(format)`
Generates a formatted report.

```javascript
const htmlReport = await projectAnalyzer.generateReport('html');
const csvReport = await projectAnalyzer.generateReport('csv');
```

---

## Usage Examples

### Basic File Analysis

```javascript
import { countLines, analyzeDirectory } from 'cloc';

// Analyze a single file
const fileStats = await countLines('./src/app.js');
console.log(`Total lines: ${fileStats.total}`);

// Analyze an entire directory
const dirStats = await analyzeDirectory('./src', {
  exclude: ['*.test.js', '*.spec.js']
});
console.log(`Total files: ${dirStats.totalFiles}`);
```

### Advanced Project Analysis

```javascript
import { ProjectAnalyzer } from 'cloc';

const analyzer = new ProjectAnalyzer('./my-project', {
  configFile: './cloc.config.js',
  outputFormat: 'json'
});

const report = await analyzer.run();

// Generate multiple report formats
await analyzer.generateReport('html');
await analyzer.generateReport('pdf');
await analyzer.generateReport('csv');
```

### Custom Language Detection

```javascript
import { FileAnalyzer } from 'cloc';

const analyzer = new FileAnalyzer({
  customPatterns: {
    'Custom Language': {
      extensions: ['.custom'],
      commentPatterns: [/^#.*$/gm, /\/\*[\s\S]*?\*\//gm]
    }
  }
});

const result = await analyzer.analyze('./script.custom');
```

### Configuration File Example

```javascript
// cloc.config.js
module.exports = {
  exclude: [
    'node_modules/**',
    '*.test.js',
    '*.spec.js',
    'coverage/**',
    'dist/**'
  ],
  include: [
    'src/**',
    'lib/**',
    'test/**'
  ],
  languages: {
    javascript: {
      extensions: ['.js', '.jsx'],
      commentStyle: '//'
    },
    typescript: {
      extensions: ['.ts', '.tsx'],
      commentStyle: '//'
    }
  },
  output: {
    format: 'json',
    file: './reports/cloc-report.json',
    includeDetails: true
  }
};
```

---

## Error Handling

All functions and methods implement comprehensive error handling:

### Common Error Types

#### `FileNotFoundError`
- **Cause**: Specified file or directory doesn't exist
- **Solution**: Verify the file path is correct and the file exists

#### `PermissionError`
- **Cause**: Insufficient permissions to read file or directory
- **Solution**: Check file permissions or run with appropriate privileges

#### `UnsupportedFileTypeError`
- **Cause**: File type is not supported for analysis
- **Solution**: Check supported languages or add custom language patterns

#### `ConfigurationError`
- **Cause**: Invalid configuration options
- **Solution**: Review configuration parameters and their expected types

### Error Handling Best Practices

```javascript
try {
  const result = await countLines('./nonexistent-file.js');
} catch (error) {
  if (error instanceof FileNotFoundError) {
    console.log('File not found, skipping...');
  } else if (error instanceof PermissionError) {
    console.log('Permission denied, check file permissions');
  } else {
    console.error('Unexpected error:', error.message);
  }
}
```

---

## Configuration

### Environment Variables

- `CLOC_CONFIG_PATH`: Path to configuration file
- `CLOC_CACHE_DIR`: Directory for caching analysis results
- `CLOC_LOG_LEVEL`: Logging level (debug, info, warn, error)
- `CLOC_MAX_FILE_SIZE`: Maximum file size to analyze (in bytes)

### Configuration Options

#### Global Configuration
```javascript
{
  maxFileSize: 10485760, // 10MB
  cacheResults: true,
  logLevel: 'info',
  ignoreHidden: true,
  followSymlinks: false
}
```

#### Language-Specific Configuration
```javascript
{
  languages: {
    javascript: {
      extensions: ['.js', '.jsx', '.mjs'],
      commentPatterns: [
        /\/\/.*$/gm,           // Single-line comments
        /\/\*[\s\S]*?\*\//gm   // Multi-line comments
      ],
      stringPatterns: [
        /"(?:[^"\\]|\\.)*"/gm,  // Double-quoted strings
        /'(?:[^'\\]|\\.)*'/gm   // Single-quoted strings
      ]
    }
  }
}
```

---

## Contributing

### Documentation Standards

When adding new public APIs, functions, or components, please follow these documentation standards:

1. **Function Documentation**: Include JSDoc comments with parameters, return values, and examples
2. **API Endpoints**: Document all endpoints with request/response examples
3. **Error Cases**: Document all possible error conditions and their causes
4. **Examples**: Provide at least one working example for each public interface
5. **Version Information**: Include version information for new features

### Example Function Documentation

```javascript
/**
 * Counts lines of code in a file with advanced filtering options
 * @param {string} filePath - Path to the file to analyze
 * @param {Object} options - Configuration options
 * @param {boolean} [options.includeComments=false] - Include comment lines
 * @param {boolean} [options.includeBlankLines=false] - Include blank lines
 * @param {string} [options.fileType] - Override file type detection
 * @returns {Promise<LineCount>} Promise resolving to line count object
 * @throws {FileNotFoundError} When file doesn't exist
 * @throws {PermissionError} When file cannot be read
 * @example
 * const count = await countLines('./src/app.js', { includeComments: true });
 * console.log(count.total); // 150
 * @since 1.0.0
 */
async function countLines(filePath, options = {}) {
  // Implementation...
}
```

### Adding New Languages

To add support for a new programming language:

1. Define language patterns in the configuration
2. Add file extension mappings
3. Include comment and string detection patterns
4. Add comprehensive tests
5. Update documentation

### Testing Documentation

All documentation examples should be tested to ensure they work correctly:

```bash
# Run documentation tests
npm run test:docs

# Validate all examples
npm run validate:examples
```

---

## Changelog

### Version 1.0.0
- Initial release with core functionality
- Support for JavaScript, TypeScript, Python, and Java
- Basic file and directory analysis
- JSON and CSV output formats

### Version 1.1.0
- Added HTML report generation
- Improved error handling
- Added caching support
- Extended language support

---

## License

This project is licensed under the MIT License. See the LICENSE file for details.

---

## Support

For questions, issues, or contributions:

- GitHub Issues: [Create an issue](https://github.com/username/cloc/issues)
- Documentation: [Full documentation](https://cloc.example.com/docs)
- API Reference: [API docs](https://cloc.example.com/api)

---

*This documentation is automatically generated and updated. Last updated: $(date)*