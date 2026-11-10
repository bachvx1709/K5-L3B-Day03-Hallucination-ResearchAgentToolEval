# Team

## Thông tin nhóm

- Tên nhóm: Nhóm L3B - VuXuanBach & NguyenHoangTrung
- Lớp: L3B
- Repo nhóm: `K5-L3B-DAY03-VuXuanBach-2A202603803-ResearchAgentToolEval`
- URL repo, nhánh nộp, commit chốt: https://github.com/bachvx1709/K5-L3B-DAY03-VuXuanBach-2A202603803-ResearchAgentToolEval.git (nhánh: NguyenHoangTrung)

## Thành viên

| STT | Họ tên | MSSV | Email | GitHub | Vai trò |
| --: | ------ | ---- | ----- | ------ | ------- |
|   1 | Vũ Xuân Bách | 2A202603803 | bachvx@example.com | bachvx1709 | Leader, Eval & Report |
|   2 | Nguyễn Hoàng Trung | 2A202603826 | 26ai.trungnh@vinui.edu.vn | trungtk03 | CP3: Custom Tool & Unit Tests |
|   3 | Nguyễn Duy Mạnh | 2A202603806 | prezzgts@gmail.com | hnamyud | Eval nhóm, Model local |

## Cá nhân

Mỗi thành viên đồng thời tạo một báo cáo riêng trong `report/` theo dạng:

```text
report/team/MSSV_HoTen.md
```

## NguyenHoangTrung-CP3

### Phần việc phụ trách

- Phụ trách toàn diện **Checkpoint 3 (CP3: Tool mới và unit test)**.
- Thiết kế, phát triển và tích hợp tool mới `source_credibility` (đánh giá độ tin cậy và phân cấp nguồn tin web).
- Đăng ký tool trong `starter_v0/tools/__init__.py` và khai báo trong `starter_v0/artifacts/tools.yaml`.
- Viết và hoàn thiện trọn bộ unit test trong `starter_v0/tests/test_tools_todo.py`, bao gồm các test cho tool mới và giải quyết tất cả stubs (đạt **0 skipped, 0 failed** trên toàn bộ 86 test cases).

### Đóng góp cụ thể

- Tạo module `starter_v0/tools/source_credibility/` với `tool.py` và `TOOL.md` chuẩn schema frontmatter.
- Hiện thực hàm `check_source_credibility(url, min_tier)` chuẩn guardrail (bắt toàn bộ ngoại lệ, trả error dict, không raise runtime exception).
- Hoàn thiện 14 test stubs cho các tool hệ thống (`clarify`, `format`, `send`, `lookup`, `fetch`, `timeline`, `social_search`, `policy`) và 5 test cases cho tool mới (`source_credibility`), kiểm tra đầy đủ happy path, input xấu, failure path, phân cấp tier và filtering.
- Đảm bảo contract test `test_tool_contract.py` pass 100%.

### Bằng chứng

- Code tool: `starter_v0/tools/source_credibility/tool.py`, `starter_v0/tools/source_credibility/TOOL.md`.
- Registry & Declaration: `starter_v0/tools/__init__.py`, `starter_v0/artifacts/tools.yaml`.
- Unit tests: `starter_v0/tests/test_tools_todo.py`.
- Kết quả test: `pytest tests/ -v` đạt **86 passed, 0 skipped, 0 failed**.

## NguyenDuyManh — CP2, model local(Bonus) và eval nhóm(CP4)

### Phần việc phụ trách

- Tối ưu mô tả và hướng dẫn tham số của tool ở bản v2.
- Chạy hai model local, thử prompt v4/v5 và kiểm tra lại v5 trên cloud.
- Viết 10 eval case nhóm, chạy đánh giá và cập nhật báo cáo, version log.

### Đóng góp và kết quả

- V2 đạt **90%** trên base eval; làm rõ cách chọn tool, hỏi lại khi thiếu thông tin và xác nhận trước khi gửi.
- Qwen 7B baseline đạt **85%**, Qwen 3B đạt **60%**. V4 trên 3B giảm xuống **25%**; rút gọn prompt ở v5 giúp tăng lên **70%**. V5 trên cloud đạt **95%**.
- Bộ group gồm **5 single turn + 5 multi turn**, có kiểm tra hai tool mới của nhóm. Run đạt **10/10 pass** theo bộ chấm; đã ghi rõ G05 vẫn trả code ngoài phạm vi và G06/G10 gặp lỗi API X 403.

### Bằng chứng

- Commit `c0b355f`: tối ưu tool declaration v2.
- Commit `3e6c80e`: thử nghiệm local và kiểm tra ngược trên cloud.
- Commit `41b6acf`: 10 case nhóm, run đánh giá và báo cáo kết quả.
- File: `starter_v0/artifacts/version_log.csv`, `starter_v0/data/eval_group.json`, các run JSON và mục B3/B7 trong `report/team/group_report.md`.
- Báo cáo cá nhân: [2A202603806_NguyenDuyManh.md](report/team/2A202603806_NguyenDuyManh.md).

### Đánh giá ngắn

Đã hoàn thành các phần việc trên và có run, commit làm minh chứng. Kết quả cho thấy prompt ngắn hơn hữu ích với model 3B trong lần thử này, nhưng các lỗi hỏi lại và xác nhận gửi vẫn còn. Khi đánh giá cần xem cả phản hồi và lỗi API, không chỉ nhìn điểm pass.
