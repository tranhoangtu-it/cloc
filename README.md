# Code Lines of Code Counter (CLOC)

Một công cụ mạnh mẽ để đếm Lines of Code (LoC) và phân tích sự thay đổi code trong các kho lưu trữ Git.

## Tính năng chính

- **Đếm Lines of Code**: Đếm chính xác LoC thực tế, dòng comment, và dòng trống cho nhiều ngôn ngữ lập trình
- **So sánh LoC giữa các commits**: So sánh sự thay đổi về LoC giữa hai commit bất kỳ
- **Phân tích theo thời gian**: Phân tích LoC trong một khoảng thời gian nhất định
- **Báo cáo chi tiết**: Tạo báo cáo dễ đọc với nhiều định dạng đầu ra

## Cài đặt

```bash
pip install -r requirements.txt
```

## Sử dụng

### Đếm LoC cho thư mục hiện tại
```bash
python cloc.py --path .
```

### So sánh LoC giữa hai commits
```bash
python cloc.py --path . --commit-id-1 abc123 --commit-id-2 def456
```

### Phân tích LoC trong khoảng thời gian
```bash
python cloc.py --path . --start-date 2024-01-01 --end-date 2024-12-31
```

### Xuất báo cáo ra file
```bash
python cloc.py --path . --output-format json --output-file report.json
```

## Cấu trúc dự án

```
cloc/
├── cloc/
│   ├── __init__.py
│   ├── counter.py          # Module đếm LoC
│   ├── git_analyzer.py     # Module phân tích Git
│   ├── reporter.py         # Module tạo báo cáo
│   ├── cli.py             # Giao diện dòng lệnh
│   └── utils.py           # Tiện ích hỗ trợ
├── tests/                 # Test cases
├── examples/              # Ví dụ sử dụng
├── requirements.txt       # Dependencies
├── setup.py              # Cài đặt package
└── README.md
```

## Ngôn ngữ được hỗ trợ

- Python
- JavaScript/TypeScript
- Java
- C/C++
- Go
- Ruby
- PHP
- C#
- Rust
- Swift
- Kotlin
- Scala
- Và nhiều ngôn ngữ khác...

## Định dạng đầu ra

- Console (mặc định)
- JSON
- CSV
- Markdown
- HTML

## Đóng góp

Mọi đóng góp đều được chào đón! Vui lòng tạo issue hoặc pull request.