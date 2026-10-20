# NTL Agent Skills

Marketplace của NTL Software cho Claude và ChatGPT/Codex. Plugin **ntl** gom skill của các phòng ban trong NTL, dùng chung một bộ style NTL. Skill của phòng ban mới được thêm vào cùng plugin này.

Skill hiện có:

| Skill | Phòng ban | Làm gì |
|---|---|---|
| `proposal` | Kinh doanh / Delivery | Deck proposal (.pptx) cho PO / khách hàng: tóm tắt, kiến trúc hiện tại, vấn đề, giải pháp, lộ trình + team + effort, chi phí hạ tầng, giả định và rủi ro |
| `training` | Đào tạo | Tài liệu đào tạo: thiết kế khóa học / topic, handbook (HTML → PDF A4), slide HTML cho workshop, quiz, kịch bản workshop |

Các skill dùng chung một bộ style NTL (màu, font, logo, cách đặt tên file, cách viết) ở `plugins/ntl/references/`, `assets/` và `scripts/`.

## Cài đặt

Hướng dẫn cài từng bước có ảnh chụp màn hình: [docs/index.html](docs/index.html). Bật GitHub Pages từ thư mục `docs/` của nhánh `main` để có link gửi cho mọi người: `https://ntlsoftvn.github.io/ntl-agent-skills/`.

### Claude Desktop

1. Mở **Customize → Browse plugins** (hoặc **Settings → Plugins**) → **Add marketplace**.
2. Dán link repo, xác nhận. Marketplace có tên `ntl`.
3. Chọn **ntl** → **Install**.
4. Mở phiên mới. Gõ yêu cầu như "soạn proposal cho dự án X" hoặc gọi thẳng `/ntl:proposal`, `/ntl:training`.

### ChatGPT / Codex Desktop

1. Mở **Plugins** → **Add marketplace** (Codex: **Plugins → Marketplaces → Add**), dán link repo.
2. Cài **ntl**. Skill dùng được trong Codex và trong ChatGPT Work trên app desktop.
3. Mở phiên mới; trong Codex gõ `/skills` để thấy `proposal`, `training`.

Tên menu có thể khác một chút theo phiên bản app.

### Không thêm được marketplace?

Người bảo trì chạy `python3 tools/pack.py` và gửi file trong `dist/`:

- **Claude Cowork:** mở `ntl.plugin` trong Cowork và bấm chấp nhận.
- **ChatGPT Work:** **Plugins → Skills → Create → Upload**, chọn `ntl-proposal.zip` hoặc `ntl-training.zip` (mỗi file là một skill đầy đủ, đã kèm style chung).

### Cập nhật / gỡ

- Cập nhật: trong app, mở marketplace `ntl` → **Update**, rồi mở phiên mới (Claude Desktop có thể cần khởi động lại).
- Từ bản 0.3.0 plugin và marketplace đổi mã định danh thành `ntl` (trước là `ntl-plugin` / `ntl-marketplace`): ai đã cài bản cũ cần gỡ plugin và marketplace cũ, thêm lại từ link repo rồi cài `ntl`.
- Gỡ: **Uninstall** `ntl`, rồi xoá marketplace nếu không dùng nữa.

## Máy cần có

| Công cụ | Dùng cho | Ghi chú |
|---|---|---|
| Python 3.9+ | `proposal` (.pptx), `training` | Có sẵn trên macOS. Lần đầu `proposal` tự cài gói `python-pptx` vào `~/.cache/ntl-agent-skills/python` (có hỏi trước) |
| Google Chrome | `training` (render PDF) | |
| *Tuỳ chọn:* poppler (`brew install poppler`) | số trang Mục lục, ảnh xem trước | Không có thì dùng `pip install pypdf` cho Mục lục |
| *Tuỳ chọn:* Keynote hoặc LibreOffice | xem trước slide .pptx | Không có thì bỏ qua bước xem trước |

## Cho người bảo trì

```
.claude-plugin/marketplace.json      danh sách plugin cho Claude
.agents/plugins/marketplace.json     danh sách plugin cho Codex / ChatGPT
plugins/ntl/
  .claude-plugin/plugin.json         định nghĩa cho Claude
  .codex-plugin/plugin.json          định nghĩa cho Codex / ChatGPT
  references/                        style chung: brand, writing, pptx, html, diagrams
  assets/                            logo, font DejaVu (+ LICENSE), style.css
  scripts/                           ntl_deck.py (pptx), build_html.py (HTML → PDF), render, compare, preview
  skills/<skill>/SKILL.md            mỗi skill; tham chiếu style chung bằng đường dẫn tương đối
tools/pack.py                        tạo file .plugin và zip skill cho app không thêm được marketplace
docs/index.html                      hướng dẫn cài đặt có ảnh chụp (GitHub Pages); logo và ảnh ở docs/assets/ (ảnh đã làm mờ lịch sử chat)
```

Thử bản local trước khi push:

```bash
claude plugin validate .
claude plugin marketplace add ./
claude plugin install ntl@ntl
codex plugin marketplace add .
codex plugin add ntl@ntl
```

Thử xong thì gỡ (`claude plugin uninstall …`, `claude plugin marketplace remove ntl`, `codex plugin remove …`, `codex plugin marketplace remove ntl`) rồi cài lại từ link GitHub. Quy tắc sửa repo ở [AGENTS.md](AGENTS.md).

Font DejaVu theo giấy phép trong `plugins/ntl/assets/fonts/LICENSE`. Template đào tạo lấy từ repo `ntl-training-hub`.
