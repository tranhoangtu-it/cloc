# cloc - Code Lines of Code Counter

## Overview

The `cloc` project is a comprehensive code analysis tool that provides detailed insights into source code metrics including line counts, complexity analysis, maintainability indices, and language detection across multiple programming languages.

## 📚 Documentation

This project includes comprehensive documentation covering all public APIs, functions, and components:

### Core Documentation Files

- **[API Documentation](./API_DOCUMENTATION.md)** - Complete API reference with examples
- **[Components Documentation](./COMPONENTS_DOCUMENTATION.md)** - Detailed component specifications
- **[Function Reference](./FUNCTION_REFERENCE.md)** - Comprehensive function documentation
- **[Documentation Style Guide](./DOCUMENTATION_STYLE_GUIDE.md)** - Guidelines for documentation maintenance

### Quick Start

```javascript
// Basic usage
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

### Key Features

- **Multi-language Support**: JavaScript, TypeScript, Python, Java, C++, and more
- **Comprehensive Analysis**: Line counts, complexity metrics, maintainability indices
- **Flexible Configuration**: Customizable file patterns and analysis options
- **Multiple Output Formats**: JSON, CSV, HTML, and PDF reports
- **Performance Optimized**: Parallel processing and intelligent caching
- **Extensible**: Plugin system for custom language support

### Installation

```bash
npm install cloc
```

### Configuration

Create a `cloc.config.js` file in your project root:

```javascript
module.exports = {
  exclude: [
    'node_modules/**',
    '*.test.js',
    '*.spec.js',
    'coverage/**'
  ],
  include: [
    'src/**',
    'lib/**'
  ],
  languages: {
    javascript: {
      extensions: ['.js', '.jsx', '.mjs'],
      commentStyle: '//'
    }
  },
  output: {
    format: 'json',
    file: './reports/cloc-report.json'
  }
};
```

### API Overview

#### Core Functions

- `countLines(filePath, options)` - Count lines in a single file
- `analyzeFile(filePath, options)` - Comprehensive file analysis
- `analyzeDirectory(directoryPath, options)` - Recursive directory analysis
- `getSupportedLanguages()` - Get list of supported languages

#### Components

- `FileAnalyzer` - Individual file analysis
- `DirectoryAnalyzer` - Directory scanning and analysis
- `ReportGenerator` - Generate reports in various formats
- `ConfigManager` - Configuration management
- `LanguageDetector` - Programming language detection

#### Utilities

- `formatBytes(bytes)` - Format file sizes
- `formatDuration(ms)` - Format time durations
- `createHash(input)` - Generate content hashes
- `debounce(func, delay)` - Debounce function calls

### Example Usage

#### Basic File Analysis

```javascript
import { countLines } from 'cloc';

const analysis = await countLines('./src/index.js', {
  includeComments: true,
  includeBlankLines: false
});

console.log(analysis);
// Output: {
//   file: './src/index.js',
//   language: 'JavaScript',
//   total: 150,
//   code: 120,
//   comments: 20,
//   blank: 10,
//   size: 4096,
//   complexity: 15
// }
```

#### Advanced Directory Analysis

```javascript
import { DirectoryAnalyzer } from 'cloc';

const analyzer = new DirectoryAnalyzer({
  recursive: true,
  exclude: ['node_modules/**', '*.test.js'],
  maxDepth: 5
});

const results = await analyzer.analyze('./my-project');
console.log(`Analyzed ${results.totalFiles} files`);
```

#### Report Generation

```javascript
import { generateReport } from 'cloc';

const report = await generateReport(analysisData, {
  format: 'html',
  template: 'detailed',
  outputPath: './reports'
});
```

### Error Handling

All functions implement comprehensive error handling:

```javascript
try {
  const result = await countLines('./nonexistent-file.js');
} catch (error) {
  if (error instanceof FileNotFoundError) {
    console.log('File not found');
  } else if (error instanceof PermissionError) {
    console.log('Permission denied');
  } else {
    console.error('Unexpected error:', error.message);
  }
}
```

### Performance

- **Parallel Processing**: Analyze multiple files concurrently
- **Intelligent Caching**: Cache results for frequently analyzed files
- **Streaming**: Handle large files efficiently
- **Memory Optimization**: Minimal memory footprint

### Contributing

Please refer to the [Documentation Style Guide](./DOCUMENTATION_STYLE_GUIDE.md) for guidelines on:

- Writing documentation
- Code examples
- API documentation standards
- Review process

### License

This project is licensed under the MIT License.

### Support

- **GitHub Issues**: Report bugs and request features
- **Documentation**: Comprehensive guides and API reference
- **Examples**: Working code examples for all features

---

*For complete documentation, please refer to the individual documentation files listed above.*