# Báo cáo cá nhân — NguyenDuyManh-2A202603806

## 1. Thông tin thành viên

- Họ tên: Nguyễn Duy Mạnh
- MSSV: 2A202603806
- Email: prezzgts@gmail.com

## 2. Phần việc phụ trách

- **Checkpoint 2 (CP2) — Tối ưu tool declaration, phiên bản v2**.
- Chuẩn hóa mô tả trong `starter_v0/artifacts/tools.yaml`: chức năng, khi nào dùng, khi nào không dùng và quy ước tham số của từng tool.
- Làm rõ ranh giới hỏi lại khi thiếu thông tin và xác nhận trước khi gửi nội dung ra ngoài.
- Chạy base eval cho v2, lưu run JSON và ghi giả thuyết, hash, kết quả vào `starter_v0/artifacts/version_log.csv`.

## 3. Đóng góp cụ thể

1. **Chuẩn hóa hướng dẫn chọn tool**:
   - Phân biệt `timeline` (bài đăng của một tài khoản) với `social_search` (bài đăng theo từ khóa/chủ đề).
   - Phân biệt `lookup` (tìm thông tin trên web) với `fetch` (đọc URL cụ thể), `papers` (tìm paper) với `paper_text` (đọc paper đã xác định).
   - Nêu rõ `format` chỉ trình bày dữ liệu đã có và `policy` dùng cho chính sách nội bộ.

2. **Làm rõ quy ước arguments và boundary**:
   - `timeline.screenname` không chứa `@`; số lượng bài đăng lấy theo yêu cầu.
   - `social_search.search_type` sử dụng `Latest` hoặc `Top` theo mục đích tìm kiếm.
   - `lookup` tách từ khóa cốt lõi khỏi `topic` và `timeframe`; tin tức hôm nay tương ứng `topic=news`, `timeframe=day`.
   - Thiếu thông tin bắt buộc thì gọi `clarify`; trước khi gửi nội dung chưa được xác nhận thì hỏi bằng `response_type=yes_no`.
   - `send` chỉ được thực hiện khi có nội dung hoàn chỉnh và người dùng đã xác nhận (`confirmed=true`).

3. **Đo và ghi nhận kết quả v2**:
   - Giả thuyết: mô tả rõ khi dùng/không dùng, boundary và quy ước args giúp giảm chọn sai tool và truyền sai tham số.
   - Run v2 đo đủ **20/20 case**, không có lỗi provider, đạt **18/20 case pass**.

   | Metric | Baseline v0 | v1 | v2 |
   |---|---:|---:|---:|
   | Case accuracy | 70% | 75% | 90% |
   | Tool routing accuracy | 90% | 90% | 95% |
   | Argument accuracy | 70% | 75% | 90% |
   | Multiturn accuracy | 83,33% | 100% | 100% |

   - Dòng v2 trong CSV ghi `metric_before=0.7`, `metric_after=0.9`: đây là so sánh case accuracy với baseline v0, tăng **20 điểm phần trăm**. Chênh lệch quan sát được so với v1 là **15 điểm phần trăm**.
   - Giữ nguyên log gốc: prompt hash của run v2 khác v1 và không khớp prompt tại commit đóng góp v2. Thông tin prompt v1 được merge vào giải thích bối cảnh bản code chung hiện tại, nhưng chưa đủ để xác định lại chính xác nội dung prompt đã dùng trong run v2. Vì vậy, không kết luận toàn bộ mức tăng chỉ đến từ thay đổi tool declaration.

## 4. Bằng chứng

- **Commit đóng góp**: `c0b355ff4f59db25333005a04760e2e40bbf924a` — `feat/Chuẩn hóa description khi nào dùng/không dùng trong tools.yaml`.
- **File đã chỉnh sửa và bằng chứng**:
  - `starter_v0/artifacts/tools.yaml`: thay đổi mô tả và hướng dẫn tham số của các tool có sẵn.
  - `starter_v0/artifacts/version_log.csv`: dòng v2, tác giả Mạnh, giả thuyết và metric trước/sau.
  - `starter_v0/runs/v2_B_base_openrouter_20261110T184219913110.json`: kết quả base eval v2.
  - `report/team/2A202603806_NguyenDuyManh.md`: báo cáo cá nhân.
- **Thông tin run v2**:
  - Provider/model: `openrouter` / `nvidia/nemotron-3.5-super-vl:free`.
  - Artifact version: `v2+peb1c8179815b+tb0d19937218b`.
  - Prompt hash: `eb1c8179815bd79d34de7d326420bb99b3072e6e8ae96464c02d4411f905fc68`.
  - Tools hash: `b0d19937218b3a8031eca337e24851191201d51ebf1f4748b502a199bbb53a11`.
  - `provider_error_cases=0`, `measured_cases=total_cases=20`: đáp ứng điều kiện run hợp lệ theo rubric.
- **AI/công cụ đã dùng và cách kiểm tra**:
  - Sử dụng ChatGPT hỗ trợ rà soát rule, đối chiếu run JSON với CSV, phân tích giới hạn của kết quả và soạn báo cáo từ bằng chứng có trong repo.
  - Đối chiếu metric tại `summary` và các case fail tại `results[*].result` trong run JSON; dùng Git kiểm tra phạm vi commit và hash artifact.
  - Trong lần rà soát sau merge, chạy từ `starter_v0/`: `.\.venv\Scripts\python.exe -B -m pytest tests/test_tool_contract.py -q -p no:cacheprovider`, kết quả **65 passed**. Đây là kiểm tra bản code hiện tại sau merge, không phải kết quả test lịch sử tại thời điểm chạy v2.

## 5. Tự đánh giá

- Đã thực hiện phần tối ưu tool declaration v2 và có commit, run JSON, dòng CSV làm bằng chứng; đây là phần đóng góp trong CP2, không phải toàn bộ các vòng v1–v3 của nhóm.
- Hai case v2 còn fail:
  - `R03_web_news_routing`: gọi đúng `lookup`, đúng `topic` và `timeframe`, nhưng `query` là `tin tức AI hôm nay nổi bật` thay vì giá trị `AI` mà eval yêu cầu. Đây là sai giá trị argument theo `observed_mismatch`, dù nhãn lỗi định sẵn của case là `wrong_tool`.
  - `R10_missing_handle`: người dùng chưa chỉ định tài khoản nhưng model gọi `timeline(screenname=sama, limit=5)` thay vì `clarify` để hỏi lại.
- Run v2 vẫn có lỗi thực thi tool HTTP 403/429 ở các lời gọi Twitter/X. Điểm 90% phản ánh lựa chọn tool và arguments theo harness, không đồng nghĩa 90% tác vụ đã lấy được dữ liệu thành công.
- Qua phần việc này, tôi rút ra rằng tool description cần chỉ rõ điều kiện sử dụng và cách điền tham số; chỉ mô tả chức năng là chưa đủ. Khi đánh giá, cần phân biệt lỗi model chọn tool/args, lỗi API của tool và ảnh hưởng của các artifact khác nhau giữa các run.
- Nếu thực hiện vòng tiếp theo, cần giữ cố định prompt và tập tool khi so sánh, tập trung một giả thuyết về hỏi lại khi thiếu tài khoản hoặc chuẩn hóa từ khóa; ghi kết quả bằng run mới và giữ nguyên bằng chứng cũ.
