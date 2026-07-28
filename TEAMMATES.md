# 👥 DANH SÁCH THÀNH VIÊN NHÓM

> Bài Lab 3: Chatbot vs ReAct Agent — Đại học VinUni

## 1. Thành viên

| STT | Họ và tên | Mã sinh viên |
| :-: | :-- | :-- |
| 1 | Nguyễn Chí Hướng | 2A202601203 
| 2 | Nguyễn Tiến Đạt | 2A202601387
| 3 | Phạm Thị Liên | 2A202601795
| 4 | Lê Quang Huy | 2A202601821

## 2. Phân công vai trò & Branch

Đề tài nhóm: **#7 — Trợ Lý Tư Vấn Khóa Học Sinh Viên** (hướng tư vấn đăng ký môn dựa trên dữ liệu sinh viên).

| Thành viên | Vai trò | Branch | File giữ | Hướng dẫn |
| :-- | :-- | :-- | :-- | :-- |
| Nguyễn Chí Hướng | Product Architect & Observability | `role1-product-architect` | `config/test_cases.json`, `docs/trace_eval.md` | [ROLE1](docs/roles/ROLE1_PRODUCT_ARCHITECT.md) |
| Nguyễn Tiến Đạt | Tool Engineer | `role2-tool-engineer` | `src/tools.py` | [ROLE2](docs/roles/ROLE2_TOOL_ENGINEER.md) |
| Phạm Thị Liên | Prompt & Safeguard Engineer | `role3-prompt-engineer` | `src/prompts.py` | [ROLE3](docs/roles/ROLE3_PROMPT_ENGINEER.md) |
| Lê Quang Huy | Core Developer / Integrator | `role4-core-developer` | `src/app.py` | [ROLE4](docs/roles/ROLE4_CORE_DEVELOPER.md) |

> Bài Lab gốc chia 5 vai; nhóm 4 người nên Role 5 (Observability) gộp vào Role 1 — người viết test case hiểu rõ nhất câu nào là bẫy nên soi trace log chính xác nhất.

## 3. Quy trình Git

Mỗi người làm trên branch riêng, giữ đúng 1 file → không conflict.

**Lần đầu — lấy branch của mình về:**

```bash
git fetch origin
git checkout role1-product-architect
```

*(đổi tên branch theo bảng trên)*

**Trong lúc làm — cập nhật code mới nhất từ main:**

```bash
git pull origin main
```

**Làm xong — đẩy lên branch của mình:**

```bash
git add .
git commit -m "Role X: cap nhat noi dung"
git push origin <ten-branch-cua-ban>
```

**Lê Quang Huy (Role 4) — gom code cả nhóm:**

```bash
git checkout main
git merge origin/role1-product-architect origin/role2-tool-engineer origin/role3-prompt-engineer
```
