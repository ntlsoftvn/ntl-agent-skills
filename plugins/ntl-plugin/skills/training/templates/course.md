# Thiết kế khóa học — <Tên khóa học 101>

Mục tiêu: đào tạo vai trò **<vai trò>** cho **<đối tượng>**. Sau khóa học, người học làm được <năng lực chính>.

Mã khóa học `<CODE101>` (chữ hoa). Cấu trúc: **course → topic**; mỗi topic có handbook PDF (và quiz, slide nếu cần) với phiên bản riêng.

## Hiện trạng

| Topic | Nội dung | Trạng thái |
|---|---|---|
| T01 | <Tên topic, 2–5 từ> — <một dòng nội dung> | Bản nháp v0.1 (MM/YYYY) |
| T02 | … | Chưa bắt đầu |

## Nguyên tắc thiết kế

- Backward design: mục tiêu đo được → câu hỏi / rubric → nội dung.
- Mỗi topic tự đứng được; ví dụ hư cấu, không dùng dữ liệu thật của khách hàng.
- Phần lõi trung lập; phần tùy biến cho từng tổ chức để riêng.
- <Quy tắc riêng của khóa, vd "Topic 01 không nêu nội dung các topic sau".>

## Danh mục topic

Mã topic `T01`, `T02`… (hoặc `<Cấp>-<NN>` nếu chia cấp). Mã không bao giờ dùng lại; topic mới lấy số kế tiếp. Đổi nội dung thì tăng phiên bản; đổi mục tiêu thì là topic mới.

| Mã | Tên topic | Cấp / thời lượng | Tiên quyết | Học liệu |
|---|---|---|---|---|
| T01 | <Tên> | <L0 · 2 giờ> | — | Handbook, quiz |

## Thuật ngữ

| English | Lần đầu (gloss tiếng Việt) | slug |
|---|---|---|
| Precondition | tiền điều kiện: điều phải đúng trước khi chạy test | precondition |

## Checklist mỗi topic

1. Viết `topics/<TOPIC>/topic.md` (mục tiêu có mã, nội dung, đánh giá).
2. `build_html.py init handbook topics/<TOPIC>/handbook`, sửa tên topic (`<title>`, `--footer-text`, cover).
3. Viết nội dung; mỗi chương một `.page`, `chnum` khớp `data-find` trong Mục lục.
4. Sơ đồ là `assets/fig-NN.svg` (NN = số hình), đúng palette; đánh số "Hình N." liên tục.
5. Build PDF, xem từng trang: ngắt trang, bảng/hình không bị cắt, không còn cảnh báo ⚠.
6. Quiz (nếu có): mỗi mục tiêu ≥ 2 câu mỗi đề, ngân hàng ≥ 3 lần; mở `#check` không còn lỗi.
7. Cập nhật bảng Hiện trạng.
