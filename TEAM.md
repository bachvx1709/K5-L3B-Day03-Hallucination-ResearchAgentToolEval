# Team

## Thông tin nhóm

- Tên nhóm: Hallucination
- Lớp: L3B
- Repo nhóm: `K5-L3B-DAY03-VuXuanBach-2A202603803-ResearchAgentToolEval`
- URL repo, nhánh nộp, commit chốt: https://github.com/bachvx1709/K5-L3B-DAY03-VuXuanBach-2A202603803-ResearchAgentToolEval

## Thành viên

| STT | Họ tên | MSSV | Email | GitHub | Vai trò |
| --: | ------ | ---- | ----- | ------ | ------- |
|   1 | Vũ Xuân Bách | 2A202603803 |26ai.bachvx2@vinuni.edu.vn| bachvx1709 | Leader, v0, v1, UI & Report |
|   2 | Nguyễn Hoàng Trung | 2A202603826 | 26ai.trungnh@vinui.edu.vn | trungtk03 | CP3: Custom Tool & Unit Tests |
|   3 | Nguyễn Duy Mạnh | 2A202603806 | 26ai.manhnd9@vinuni.edu.vn | hnamyud | Eval nhóm, Model local |
|   4 | Nguyễn Tuấn Dũng | 2A202603859 | 26ai.dungnt16@vinuni.edu.vn | DungNguyen74 | CP3: Custom Tool (text_stats) & Unit Tests |

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

## VuXuanBach — Leader, CP1 (v0), CP2 (v1), UI & Report

### Phần việc phụ trách

- **Leader**: Điều phối nhóm, phân chia công việc, tổ chức cấu trúc dự án và review tiến độ.
- **CP1 & CP2 (v0, v1)**:
  - Thiết lập baseline `v0` ban đầu trên benchmark `eval_base.json`.
  - Tối ưu hóa phiên bản `v1` cho Checkpoint 2 (CP2) tập trung vào `system_prompt.md`.
- **Phát triển UI & Deployment**:
  - Xây dựng giao diện chat đa lượt trực quan với Streamlit (`starter_v0/app.py`).
  - Thiết lập public endpoint phục vụ Team Showdown qua Cloudflare Tunnel.
- **Tổng hợp Báo cáo nhóm (`group_report.md`)**:
  - Thu thập số liệu, đối chiếu bằng chứng thực tế từ run JSON, transcript và unit test để hoàn thiện toàn diện báo cáo nhóm.

### Đóng góp và kết quả

- **Baseline v0**: Ghi nhận độ chính xác cơ sở 70% (14/20 cases pass) trên model `nvidia/nemotron-3.5-super-vl:free` (OpenRouter); phân loại chi tiết các lỗi hallucination/boundary (R03, R10, R11, R12, R13, M02).
- **Phiên bản v1**: Thêm các chỉ dẫn cấm đoán mò thông tin thiếu và bắt buộc hỏi xác nhận Yes/No trước khi xuất bản ra bên ngoài vào `system_prompt.md`, nâng accuracy từ 70% lên 75% (15/20 cases pass).
- **UI Streamlit & Tunnel**: Phát triển hoàn chỉnh `starter_v0/app.py`, kết nối trực tiếp với OpenRouterProvider, hỗ trợ tương tác đa lượt, hiển thị trực quan các lượt gọi tool và tự động lưu transcript. Deploy thành công qua Cloudflare Tunnel phục vụ Showdown.
- **Báo cáo nhóm**: Tổng hợp và hoàn thiện toàn bộ báo cáo `report/team/group_report.md` (Phần A giới thiệu agent và Phần B chi tiết bằng chứng B1–B7).

### Bằng chứng

- **Files**: `starter_v0/artifacts/system_prompt.md`, `starter_v0/artifacts/version_log.csv`, `starter_v0/app.py`, `report/team/group_report.md`.
- **Runs**:
  - Baseline v0: `starter_v0/runs/v0_B_base_openrouter_20261110T172108091238.json` (70%).
  - Prompt v1: `starter_v0/runs/v1_B_base_openrouter_20261110T193325762444.json` (75%).
- **Public URL**: `https://geography-adaptive-leaves-unfortunately.trycloudflare.com`.
- **Báo cáo cá nhân**: [2A202603803_VuXuanBach.md](report/team/2A202603803_VuXuanBach.md).

## NguyenTuanDung-2A202603859

### Phần việc phụ trách

- Phụ trách **Checkpoint 3 (CP3: Tool mới và unit test)** — xây dựng tool `text_stats`.
- Thiết kế, hiện thực và tích hợp tool mới `text_stats` (đếm số từ, số ký tự và ước tính thời gian đọc cho văn bản hoặc bản nháp).
- Đăng ký tool vào `TOOL_FUNCTIONS` trong `starter_v0/tools/__init__.py` và khai báo schema trong `starter_v0/artifacts/tools.yaml`.
- Viết unit test cho `text_stats` và hoàn thiện toàn bộ các stub test trong `starter_v0/tests/test_tools_todo.py` (trên nhánh `Dungv2`, commit `0b0adce`).
- Viết báo cáo cá nhân `report/team/2A202603859_NguyenTuanDung.md` và cập nhật nội dung đóng góp tương ứng trong `report/team/group_report.md`.

### Đóng góp cụ thể

- Tạo module `starter_v0/tools/text_stats/` gồm `tool.py` và `Tool.md` (frontmatter `name: text_stats`, `category: analysis`, `requires_env: []`, mô tả `Purpose`, `When to use`, `Arguments`).
- Hiện thực hàm `text_stats(text: str, wpm: int = 200) -> Dict[str, Any]` tính `word_count`, `char_count`, `estimated_reading_seconds` và `items`, kèm guardrail kiểm tra `text` rỗng/sai kiểu và `wpm` không phải số nguyên hoặc `<= 0` để trả về error dict (`status: "error"`, `items: []`) thay vì raise exception.
- Đăng ký `"text_stats": text_stats` trong `starter_v0/tools/__init__.py` và khai báo schema trong `starter_v0/artifacts/tools.yaml` (nêu rõ `USE WHEN` / `DO NOT USE WHEN` và ràng buộc tham số).
- Hoàn thiện 14 test stubs cho các tool có sẵn (`clarify`, `format`, `send`, `lookup`, `fetch`, `timeline`, `social_search`, `policy`) và viết 3 unit tests cho `text_stats` (happy path, input chuỗi khoảng trắng rỗng, `wpm=0` và `wpm="invalid_int"`) ở commit `0b0adce` (nhánh `Dungv2`, đã merge vào `main` qua PR #3 `7eaba02`). *(Ghi chú: sau khi merge PR #2 `4746c85`, `starter_v0/tests/test_tools_todo.py` trên `main` hiện giữ 1 test của `text_stats` là `test_text_stats_failure_invalid_wpm_returns_error_dict` cùng bộ test của `source_credibility` và 14 test hệ thống.)*

### Bằng chứng

- Code tool: `starter_v0/tools/text_stats/tool.py`, `starter_v0/tools/text_stats/Tool.md`.
- Registry & Declaration: `starter_v0/tools/__init__.py`, `starter_v0/artifacts/tools.yaml`.
- Unit tests: `starter_v0/tests/test_tools_todo.py` (commit `0b0adce`, nhánh `Dungv2`, merge `7eaba02`).
- Báo cáo: `report/team/2A202603859_NguyenTuanDung.md`, `report/team/group_report.md` (commit `8719799`).
- Kết quả test ghi nhận trong báo cáo cá nhân (khi chạy trên nhánh `Dungv2` trước lúc gộp PR #2): `pytest tests/ -v` đạt **84 passed, 0 failed, 0 skipped** (60 contract tests, 7 example tests, 17 tests trong `test_tools_todo.py`).

### Tự đánh giá

- Hoàn thành đầy đủ các hạng mục của **Checkpoint 3 (CP3)** đối với tool `text_stats` (code có guardrail trả error dict, tài liệu đặc tả, đăng ký trong `__init__.py` và `tools.yaml`, thiết kế đủ ≥ 3 unit tests theo 3 nhóm happy path / input xấu / nhánh lỗi) và hoàn thiện phần Test Challenge (0 skipped, 0 failed) trên nhánh `Dungv2`.
- Các điểm cần xử lý tiếp trên nhánh `main` để đảm bảo chấm tự động ổn định:
  - Đổi tên `starter_v0/tools/text_stats/Tool.md` thành `TOOL.md` (in hoa) để đảm bảo `test_tool_folder_has_tool_md_with_matching_name` (`glob("*/TOOL.md")`) pass trên môi trường phân biệt chữ hoa/thường (Linux).
  - Khôi phục 2 unit tests của `text_stats` bị mất khi merge PR #2 (`test_text_stats_happy_path_returns_counts` và `test_text_stats_bad_input_empty_string_from_model` khớp với chữ ký và error dict của `tool.py`) vào `starter_v0/tests/test_tools_todo.py` trên `main` để đạt đủ ≥ 3 unit tests cho mỗi tool mới theo rubric C4.
