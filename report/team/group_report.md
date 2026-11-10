# Báo cáo nhóm — Day 03 Research Agent Tool Eval

> Báo cáo gồm 2 phần có hạn khác nhau:
> - **Phần A (mục 2)** — giới thiệu agent, ngắn gọn 1 trang. **Xong trước Team showdown (16:30)** để team khác hiểu nhanh agent có tool gì, làm được gì. Có thể làm thêm poster `report/team/poster.html` hoặc `poster.svg`.
> - **Phần B (mục 3–7)** — chi tiết và bằng chứng, dựa trên log thật. Hoàn thiện trước deadline nộp bài.
>
> Mỗi bảng phải trỏ được tới file thật: run JSON, transcript, commit. Cách chấm xem [RUBRIC.md](../../RUBRIC.md).

## 1. Thông tin nhóm

- Tên nhóm: Hallucination
- Thành viên và phân công: xem [TEAM.md](../../TEAM.md)
- Provider/model dùng cho v0–v3: nvidia/nemotron-3.5-super-vl:free

## 2. Mục tiêu và cách tiếp cận — PHẦN A: Giới thiệu agent

### A1. Agent này làm được gì

> 1–2 câu mô tả agent dùng để làm gì (cho team khác hiểu nhanh).

Ví dụ: "Research agent: tìm tin theo từ khóa / theo tài khoản, đọc URL, tổng hợp thành digest, và gửi lên Telegram khi được xác nhận."

**Cách chạy UI:**

> Lệnh chạy UI (ví dụ `streamlit run app.py`) và dependency đã thêm vào `starter_v0/requirements.txt`.

**Link dùng thử (deploy):**

> Dán link public để team khác mở thử ngay. Cách deploy nhanh bằng Cloudflare Tunnel xem README. Nếu deploy Vercel/Streamlit Cloud thì dán link đó.
>
> URL:

### A2. Tool agent có

> Liệt kê các tool agent đang dùng (gồm tool mới nhóm tự thêm). Mỗi tool 1 dòng: tên + làm được gì.

| Tên tool | Làm được gì | Tool mới nhóm thêm? |
|---|---|---|
| clarify | hỏi lại người dùng khi thiếu thông tin | không |
| timeline | lấy bài đăng gần đây của tài khoản X/Twitter | không |
| social_search | tìm kiếm bài đăng trên mạng xã hội | không |
| lookup | tra cứu tin tức và thông tin trên web | không |
| fetch | cào nội dung chi tiết từ một URL | không |
| format | trình bày dữ liệu thành văn bản bản tin | không |
| send | gửi tin nhắn lên Telegram sau xác nhận | không |
| policy | tra cứu tài liệu quy định nội bộ công ty | không |
| papers | tìm kiếm bài báo khoa học trên arXiv | không |
| paper_text | trích xuất text PDF từ bài báo arXiv | không |
| source_credibility | thẩm định độ tin cậy và phân cấp nguồn tin của URL | Có (Nguyễn Hoàng Trung) |
| text_stats | tính số từ, số ký tự và thời gian đọc ước tính cho văn bản | Có (Nguyễn Tuấn Dũng) |

### A3. Câu hỏi mẫu để thử

> 3–5 câu hỏi/yêu cầu mẫu để team khác tự thử agent ngay.

1.
2.
3.

## 3. Giải pháp

> Tóm tắt các thay đổi chính trong `starter_v0/artifacts/system_prompt.md` và `starter_v0/artifacts/tools.yaml`, và tool mới nhóm viết (tên, làm gì, khi nào agent nên gọi).

- **Tool mới do Nguyễn Hoàng Trung thực hiện (CP3): `source_credibility`**:
  - *Chức năng*: Kiểm tra và phân cấp độ tin cậy của tên miền/URL (`academic`, `verified_news`, `tech_media`, `community`, `unverified`), tính toán điểm độ tin cậy (0.0 - 1.0) và đưa ra khuyến nghị cách sử dụng nguồn tin.
  - *Khi nào agent nên gọi*: Khi người dùng hoặc luồng nghiên cứu cần xác minh tính xác thực, kiểm tra nguồn gốc bài viết trước khi trích dẫn hoặc tổng hợp thành báo cáo/digest chính thức.
  - *Thiết kế an toàn (Guardrail)*: Xử lý chuẩn hóa tên miền, bắt toàn bộ ngoại lệ và trả về error dict dạng `{"tool": "source_credibility", "error": ..., "message": ...}` thay vì raise runtime error làm crash agent.
  - *Tích hợp*: Đăng ký trong `starter_v0/tools/__init__.py`, khai báo schema trong `starter_v0/artifacts/tools.yaml`, kèm file tài liệu đặc tả `starter_v0/tools/source_credibility/TOOL.md`.
  - *Kiểm thử*: Đã viết 5 unit test chuyên biệt và hoàn thiện toàn bộ các stubs trong `starter_v0/tests/test_tools_todo.py`, đạt kết quả toàn suite `pytest` 86 passed, 0 skipped, 0 failed.
- **Tool mới `text_stats` (Nguyễn Tuấn Dũng - 2A202603859, CP3)**:
  - **Làm gì**: nhận `text` (chuỗi không rỗng) và `wpm` (mặc định 200 từ/phút, > 0), trả về số từ (`word_count`), số ký tự (`char_count`) và thời gian đọc ước tính theo giây (`estimated_reading_seconds`). Nếu input rỗng/sai kiểu hoặc `wpm <= 0`, tool trả về error dict (`status: "error"`) thay vì raise exception.
  - **Khi nào agent nên gọi**: khi người dùng yêu cầu đếm từ/ký tự, kiểm tra độ dài đoạn tóm tắt/bản nháp hoặc ước tính thời gian đọc (ví dụ trước khi gửi); không dùng để tìm kiếm web hay đọc URL.
  - **Tích hợp**: khai báo trong `starter_v0/artifacts/tools.yaml`, đăng ký trong `starter_v0/tools/__init__.py`, mô tả tại `starter_v0/tools/text_stats/Tool.md` (`starter_v0/tools/text_stats/tool.py`).

## 4. Kết quả — PHẦN B: Chi tiết và bằng chứng

### B1. Version Evidence

Lấy từ `starter_v0/artifacts/version_log.csv` và `starter_v0/runs/*.json`. Chỉ dùng run có `provider_error_cases == 0` và `measured_cases == total_cases`.

| Version | Changed Artifact | Hypothesis | Metric Before | Metric After | Run File |
|---|---|---|---:|---:|---|
| v0 | baseline |  |  |  |  |
| v1 |  |  |  |  |  |
| v2 |  |  |  |  |  |
| v3 |  |  |  |  |  |

### B2. Failure Analysis

Lấy từ `results[*].result.failures` trong run JSON.

| Case ID | Failure Type | Actual Tool Calls | What Failed | Fix |
|---|---|---|---|---|
|  |  |  |  |  |

### B3. Team Eval Cases

Bộ `starter_v0/data/eval_group.json` gồm **10 case: 5 single turn + 5 multi turn**. Chạy bằng **v3 / nvidia/nemotron-3.5-super-vl:free (OpenRouter)**, bằng chứng: [v3_B_group_openrouter_20261110T234627302520.json](../../starter_v0/runs/v3_B_group_openrouter_20261110T234627302520.json).

Run đo đủ **10/10 case**, không có lỗi provider. Case accuracy, tool routing, argument và multiturn đều đạt **100%** theo bộ chấm hiện tại.

| Case ID | What It Tests | Expected Tool/Behavior | Result |
|---|---|---|---|
| `G01_source_credibility_routing` | Single: đánh giá uy tín nguồn | `source_credibility(url=https://arxiv.org/)` | PASS |
| `G02_text_stats_routing` | Single: đếm từ/ký tự, thời gian đọc | `text_stats(đoạn đã cho, wpm=150)` | PASS |
| `G03_missing_article_url` | Single: thiếu URL bài báo | `clarify(response_type=text)` | PASS |
| `G04_confirm_prepared_digest` | Single: xác nhận trước khi đăng | `clarify(response_type=yes_no), không send` | PASS |
| `G05_out_of_scope_code` | Single: yêu cầu code ngoài phạm vi | `Không gọi tool` | PASS theo eval; vẫn viết code, cần xem lại nội dung |
| `G06_correct_handle_and_keep_limit` | Multi: sửa tài khoản, giữ số lượng | `timeline(screenname=SpaceX, limit=4)` | PASS routing/args; API X lỗi 403 |
| `G07_switch_social_to_web` | Multi: chuyển X sang tin web | `lookup(query=NVIDIA, topic=news, timeframe=month)` | PASS |
| `G08_replace_text_keep_reading_speed` | Multi: thay đoạn văn, giữ tốc độ đọc | `text_stats(đoạn mới, wpm=180)` | PASS |
| `G09_replace_url_before_fetch` | Multi: chỉ đọc URL đã sửa | `fetch(url=https://www.iana.org/domains/reserved)` | PASS |
| `G10_change_social_sort_and_count` | Multi: đổi sắp xếp và số bài | `social_search(query=Kubernetes, search_type=Top, limit=3)` | PASS routing/args; API X lỗi 403 |

Ba case G01, G02 và G08 kiểm tra routing tới tool mới của nhóm (`source_credibility`, `text_stats`). G01 nhận diện nguồn arXiv ở mức `academic`; G02 trả 10 từ, 43 ký tự, 4 giây đọc; G08 dùng đúng đoạn thay thế và trả 8 từ, 40 ký tự, khoảng 2,7 giây đọc.

**Đánh giá thêm từ log:** G05 pass vì bộ chấm chỉ kiểm tra không gọi tool, nhưng model vẫn viết hàm quicksort thay vì từ chối yêu cầu ngoài phạm vi. Vì vậy chưa thể kết luận boundary nội dung đã đúng. G06 và G10 pass về tên tool/tham số nhưng API X trả HTTP 403, chưa lấy được dữ liệu. `provider_error_cases=0` chỉ nói không lỗi ở bước gọi model, không có nghĩa mọi tool đều chạy thành công. G04 hỏi xác nhận đúng và không gọi send; run này không phải bằng chứng gửi Telegram thật.

Bộ group bổ sung các tình huống cụ thể, không thay thế base eval. G04 có sẵn nội dung và yêu cầu hỏi xác nhận rõ hơn R12 của base suite, nên G04 pass không chứng minh đã sửa được R12. Các case multi turn chỉ chấm lời gọi tool cho yêu cầu cuối dựa trên ngữ cảnh trước đó.

### B4. Live Chat Evidence

Lấy từ `starter_v0/transcripts/*.transcript.json`.

| Turn | User Request | Tool Calls | Version Evidence | Outcome |
|---|---|---|---|---|
|  |  |  |  |  |

### B5a. Required Evidence — Tool mới, unit test, UI

| Item | Evidence File | What Worked | Risk / Guardrail |
|---|---|---|---|
| Tool mới (`tools/<tên>/`) | `starter_v0/tools/source_credibility/` (`tool.py`, `TOOL.md`) | Phân cấp uy tín chính xác cho học thuật, tin tức, lab công nghệ và MXH | Bắt mọi ngoại lệ (URL rỗng, DNS lỗi), trả error dict, không raise runtime error |
| Unit test tool mới (≥ 3 test/tool) | `pytest tests/ -v` output (0 failed, 0 skipped: 86 passed) | 5 tests cho tool mới (happy path, input rỗng/xấu, failure path, domain lạ, filter tier) | Chạy 100% offline, mock đầy đủ với fake_http và monkeypatch |
| UI (lệnh chạy + link dùng thử) |  |  |  |

**Tool unit tests (do Nguyễn Hoàng Trung phụ trách):**
- Đã viết 5 test chuyên biệt cho `source_credibility` và hoàn thiện toàn bộ 14 stubs hệ thống trong `starter_v0/tests/test_tools_todo.py` (tổng 19 tests trong file này, toàn bộ suite đạt 86 passed, 0 skipped, 0 failed).
- **Ví dụ lỗi mà unit test bắt được nhưng eval không bắt được**: Khi model truyền đối số rỗng `url=""` hoặc `url=None` hoặc URL không có scheme `https://`, eval case thông thường chỉ so khớp xem model có gọi đúng tên tool không chứ không chạy sâu kiểm tra độ ổn định của hàm. Unit test bắt được việc hàm chuẩn hóa dữ liệu, bọc an toàn và trả về error dict dạng `{"tool": "source_credibility", "error": "ValueError", "message": "URL string must be provided and cannot be empty."}` thay vì để hàm văng unhandled Exception làm crash quy trình thực thi của Agent.
| Tool mới (`tools/<tên>/`) | `starter_v0/tools/text_stats/tool.py`, `Tool.md`, `starter_v0/tools/__init__.py`, `starter_v0/artifacts/tools.yaml` | Tính chính xác `word_count`, `char_count`, `estimated_reading_seconds` (hỗ trợ ép kiểu `wpm` dạng chuỗi như `"200"`), khớp contract test | Kiểm tra `text` rỗng/không phải `str`, `wpm` không phải số nguyên hoặc `<= 0` → trả error dict (`status: "error"`, `items: []`), không raise exception |
| Unit test tool mới (≥ 3 test/tool) | `starter_v0/tests/test_tools_todo.py`, `pytest tests/ -v` (`84 passed in 0.96s`, 0 failed, 0 skipped) | 3 tests cho `text_stats` (happy path, input chuỗi khoảng trắng rỗng, `wpm=0` và `wpm="invalid_int"`) + 14 tests cho các tool có sẵn đều pass | Toàn bộ suite chạy offline qua `fake_http` và `monkeypatch` (`block_network` chặn mọi request thật) |
| UI (lệnh chạy + link dùng thử) |  |  |  |

Tool unit tests: Đã viết 3 unit tests cho `text_stats` và hoàn thiện 14 test stubs cho các tool có sẵn (`clarify`, `format`, `send`, `lookup`, `fetch`, `timeline`, `social_search`, `policy`) trong `starter_v0/tests/test_tools_todo.py` (tổng 17 tests trong file này; toàn bộ suite `pytest tests/ -v` đạt **84 passed, 0 failed, 0 skipped**). Ví dụ lỗi mà unit test bắt được nhưng eval không bắt được: eval chỉ chấm việc model có gọi đúng tên tool và subset tham số hay không, còn unit test (`test_text_stats_bad_input_empty_string_from_model`, `test_text_stats_failure_invalid_wpm_returns_error_dict`) kiểm chứng trực tiếp rằng khi model truyền chuỗi toàn khoảng trắng `"   "`, `wpm=0` hoặc `wpm="invalid_int"`, hàm vẫn xử lý an toàn và trả về error dict có `status == "error"` thay vì văng lỗi làm gián đoạn agent.

### B5. Bonus Evidence

Chỉ điền nếu nhóm làm bonus (ghi riêng, tối đa 10 điểm). Tool có sẵn (`send`, `policy`, `papers`, `paper_text`) không tự được bonus.

| Bonus | Evidence File | What Worked | Risk / Guardrail |
|---|---|---|---|
| Small Local Model | xem B7 |  |  |
| Hơn 3 tool mới (≥ 4) |  |  |  |
| `send` gửi thật lên Telegram sau xác nhận | transcript |  |  |
| Test challenge (0 skipped / regression test) | `pytest tests/ -v` output | Giải quyết toàn bộ 14 stubs kiểm thử của tool có sẵn + 5 test tool mới, đưa test suite về 86 passed, 0 failed, 0 skipped | 100% test chạy offline qua fake_http và monkeypatch |

Test challenge: Đã hoàn thiện toàn bộ stubs trong `starter_v0/tests/test_tools_todo.py`, xử lý chính xác cơ chế lọc và trust boundary của `search_company_policy` (bóc tách `untrusted_text` cho các câu lệnh can thiệp prompt), mock trích xuất PDF/firecrawl/twitter/tavily/telegram, đưa tỷ lệ skipped của toàn suite về đúng 0.
| Test challenge (0 skipped / regression test) | `starter_v0/tests/test_tools_todo.py`, `pytest tests/ -v` (`84 passed, 0 failed, 0 skipped`) | Hoàn thiện toàn bộ 14 stubs cho tool có sẵn (`clarify`, `format`, `send`, `lookup`, `fetch`, `timeline`, `social_search`, `policy`) + 3 tests cho `text_stats` | 100% offline với `fake_http` và `monkeypatch`, kiểm tra cả request gửi đi, mapping kết quả, guardrail `send` và trust boundary `policy` |

Test challenge: Đã hoàn thiện toàn bộ 14 stubs trong `starter_v0/tests/test_tools_todo.py` để toàn bộ test suite đạt **84 passed, 0 failed, 0 skipped** (không phát hiện bug cần sửa trong code của các tool có sẵn; tất cả assert hành vi hiện tại đều pass).

### B7. Small Local Model Challenge (bonus)

Nhóm chạy hai model local khác kích thước: **Qwen 2.5 7B** và **Qwen 2.5 3B** qua Ollama. Sau đó thử hai vòng tối ưu trên 3B và chạy bản v5 trên cloud để kiểm tra ngược. Các run trong bảng đều đo đủ **20/20 case**, không có lỗi provider. Các điểm dưới đây là phần trăm.

| Version | Model (provider) | Prompt/Tools | case_accuracy | tool_routing | argument | multiturn | Run File |
|---|---|---|---:|---:|---:|---:|---|
| v3 | nvidia/nemotron-3.5-super-vl:free (openrouter) | v3 cloud | 95.00% | 100.00% | 95.00% | 100.00% | [v3_B_base_openrouter_20261110T190653600689.json](../../starter_v0/runs/v3_B_base_openrouter_20261110T190653600689.json) |
| v3-qwen7b | qwen2.5:7b (ollama) | v3 local baseline | 85.00% | 85.00% | 85.00% | 100.00% | [v3-qwen7b_B_base_ollama_20261110T221831415809.json](../../starter_v0/runs/v3-qwen7b_B_base_ollama_20261110T221831415809.json) |
| v3-qwen3b | qwen2.5:3b (ollama) | v3 local baseline | 60.00% | 70.00% | 60.00% | 66.67% | [v3-qwen3b_B_base_ollama_20261110T230616136972.json](../../starter_v0/runs/v3-qwen3b_B_base_ollama_20261110T230616136972.json) |
| v4-local-qwen3b | qwen2.5:3b (ollama) | local v4 | 25.00% | 50.00% | 25.00% | 16.67% | [v4-local-qwen3b_B_base_ollama_20261110T231409802552.json](../../starter_v0/runs/v4-local-qwen3b_B_base_ollama_20261110T231409802552.json) |
| v5-local-qwen3b | qwen2.5:3b (ollama) | local v5 | 70.00% | 70.00% | 70.00% | 83.33% | [v5-local-qwen3b_B_base_ollama_20261110T231815632353.json](../../starter_v0/runs/v5-local-qwen3b_B_base_ollama_20261110T231815632353.json) |
| v5-local-cloud | nvidia/nemotron-3.5-super-vl:free (openrouter) | local v5 | 95.00% | 100.00% | 95.00% | 100.00% | [v5-local-cloud_B_base_openrouter_20261110T233320041735.json](../../starter_v0/runs/v5-local-cloud_B_base_openrouter_20261110T233320041735.json) |

**Lưu ý khi so sánh:** Hai baseline local có cùng prompt hash `131a920b599e` và tools hash `837e452d8ec9`, nhưng khác run v3 cloud (`dd22a4e2a8aa` / `141d5f5ff0e9`). Vì vậy, chênh lệch với v3 cloud chưa thể quy hoàn toàn cho model. Các run local v3–v5 giữ nguyên tools hash; v5 local và v5 cloud có cùng cả prompt/tools hash. Bản v3 cloud không bị sửa khi tạo các file local riêng.

**Lỗi của baseline local (đếm theo case trong run JSON):**

| Failure Pattern | Qwen 7B | Qwen 3B | Example Case | Fix Tried | Helped? |
|---|---:|---:|---|---|---|
| Chọn sai tool thay tool cần dùng | 1 | 3 | 7B: R10; 3B: R10, R13, M06 | v4 nhấn mạnh clarify; v5 rút gọn routing | Chưa sửa được các case này |
| Bịa tên tool không được khai báo | 0 | 0 | Không ghi nhận | Giữ nguyên bộ tools | Chưa có lỗi để đánh giá |
| JSON args lỗi (`_invalid_json_arguments`) | 0 | 0 | Không ghi nhận | Giữ nguyên bộ tools | Chưa có lỗi để đánh giá |
| Không gọi tool, chỉ hỏi bằng text | 2 | 2 | R11, R12 | v4 yêu cầu gọi clarify thực tế | Không; v4/v5 chuyển sang gọi sai tool |
| Bỏ qua tool clarify cần gọi | 3 | 3 | R10, R11, R12 | v4 thêm quy tắc clarify, v5 viết ngắn hơn | Cả ba case vẫn fail |
| Gọi thừa khi phải không dùng tool | 0 | 1 | 3B: R14 gọi clarify cho câu coding ngoài phạm vi | v5 giữ quy tắc không gọi tool | Chưa cải thiện |
| Lặp cùng tên tool trong một case | 0 | 0 | Không ghi nhận | v5 nhắc tránh gọi lặp | Chưa có lỗi để đánh giá |
| Sai/thiếu giá trị args ở tool đúng | 0 | 2 | 3B: R06, M02 | v5 nêu ngắn gọn topic=news và giữ ngữ cảnh | Có, cả hai case pass ở v5 |

Các nhóm trên có giao nhau, không cộng để tính tổng case fail. “Gọi thừa” ở đây chỉ đếm case yêu cầu không dùng tool; gọi sai tool thay thế được tính ở hàng đầu. Bảng dựa trên `actual_tool_calls`, `actual_text` và `failures`, không chỉ dựa vào nhãn `failure_type` có sẵn.

So với những case cloud v3 pass, 7B fail thêm **R10, R11**; 3B fail thêm **R06, R10, R11, R13, R14, M02, M06**. R12 là case cả cloud và local đều fail nhưng khác biểu hiện: local hỏi bằng text, cloud gọi clarify với `response_type="text"` thay vì `"yes_no"`.

**Hai vòng tối ưu đã thử:**

- **v4-local — giả thuyết:** nhấn mạnh phải gọi clarify qua giao diện tool sẽ giảm việc hỏi bằng text hoặc đoán thông tin. Nhóm thêm phần hướng dẫn này vào `system_prompt_local_v4.md`, dùng `tools_local_v4.yaml` là bản sao tools baseline. Kết quả giảm từ **60% xuống 25%**, ba case R10–R12 vẫn fail. Giả thuyết chưa được kết quả ủng hộ.
- **v5-local — giả thuyết:** prompt ngắn và ít lặp giúp model nhỏ làm đúng hơn. Nhóm rút prompt v4 từ **739 xuống 322 từ**, giữ các quy tắc routing, tham số, xác nhận và cùng bộ tools. Kết quả tăng từ **25% lên 70%**, cao hơn baseline **10 điểm phần trăm**. V5 không dùng bộ ví dụ hội thoại few-shot riêng; thay đổi chính là cách viết prompt ngắn gọn hơn.

**Điều gì giúp model nhỏ nhất?** Trong các lần chạy này, bản prompt rút gọn v5 cho kết quả tốt nhất trên 3B. So với baseline, v5 sửa được R06 và M02 nhờ điền đúng `topic="news"`; điểm hội thoại nhiều lượt tăng từ **66,67% lên 83,33%**. Routing vẫn **70%**, nên cải thiện chủ yếu nằm ở tham số và giữ ngữ cảnh. Đây là bằng chứng cho bản v5 đã thử, chưa đủ để kết luận mọi prompt ngắn đều tốt hơn.

V5 vẫn fail **R10, R11, R12, R13, R14, M06**. Dù tập case fail ít hơn baseline, hành vi R11/R12 xấu đi: R11 tự tạo URL để gọi fetch; R12 gọi `send(confirmed=false)` thay vì clarify. Tool send trả `needs_confirmation`, nên run này **không cho thấy tin đã được gửi**. Không nên dùng điểm tổng cao hơn để bỏ qua các lỗi này.

**Kiểm tra ngược trên cloud:** Bản local v5 đạt **95%**, bằng v3 cloud; routing **100%**, argument **95%**, multiturn **100%**. Cloud vẫn fail R12 do hỏi nội dung với `response_type="text"` thay vì xác nhận `"yes_no"`. Như vậy v5 giữ được điểm cloud trong lần chạy này, nhưng chưa phải bản giải quyết tốt mọi boundary cho cả hai loại model. Run cloud hiện có là kết quả sau khi chạy lại, đủ 20 case và không còn lỗi provider; không dùng điểm từ lượt bị quota trước đó để kết luận.

**Khi nào chọn local?** Local phù hợp để thử nghiệm hoặc xử lý yêu cầu nghiên cứu đơn giản khi muốn giảm việc gửi dữ liệu tới model cloud. Trong baseline cùng artifact, 7B đạt 85%, cao hơn 3B 60%; tuy nhiên chưa chạy v5 trên 7B nên chưa biết bản đó cải thiện bao nhiêu. Với yêu cầu thiếu thông tin hoặc gửi nội dung ra ngoài, cả hai local vẫn cần được kiểm tra kỹ và có người xác nhận. Các tool tìm kiếm của lab vẫn gọi dịch vụ bên ngoài, nên dùng model local không đồng nghĩa toàn bộ luồng chạy offline.

## 5. Khó khăn và cách xử lý

> Khó khăn chính và cách nhóm xử lý. Nếu gặp lỗi kỹ thuật (provider lỗi, hết quota API, tool không chạy), mô tả lỗi và dẫn bằng chứng: run JSON, log, ảnh chụp.

-

- **API X trả HTTP 403:** G06 (`timeline`) và G10 (`social_search`) trong [run group v3](../../starter_v0/runs/v3_B_group_openrouter_20261110T234627302520.json) chọn đúng tool/tham số nhưng không lấy được dữ liệu. Nhóm giữ nguyên log và tách lỗi API tool khỏi điểm routing/args; chưa có bằng chứng khắc phục lỗi quyền truy cập.

## 6. Tổng hợp đóng góp

Chi tiết đóng góp của từng thành viên nằm trong [TEAM.md](../../TEAM.md) và các báo cáo cá nhân `report/team/MSSV_HoTen.md`:

- **Nguyễn Tuấn Dũng (`2A202603859`)**: hoàn thành CP3 — tool mới `text_stats` và hoàn thiện toàn bộ `starter_v0/tests/test_tools_todo.py` (84 passed, 0 failed, 0 skipped). Xem chi tiết tại [2A202603859_NguyenTuanDung.md](./2A202603859_NguyenTuanDung.md).

## 7. Hạn chế và hướng cải thiện — B6. Reflection

- Fix nào thuộc `system_prompt.md`?
- Fix nào thuộc `tools.yaml`?
- Failure nào cần review thủ công thay vì chấm tự động?
- Nếu có thêm một vòng, nhóm sẽ thử giả thuyết nào?

## 8. Tài liệu tham khảo

-
