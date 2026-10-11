import random
import time
import streamlit as st

st.set_page_config(page_title="Đấu Trí Toán 8", page_icon="📐")


# Hàm tạo câu hỏi Toán lớp 8 ngẫu nhiên
def generate_question():
  category = random.choice([
      "HangDangThuc",
      "DaThuc",
      "PhuongTrinh",
      "HinhHoc",
  ])

  if category == "HangDangThuc":
    # Câu hỏi về Hằng đẳng thức đáng nhớ
    a = random.randint(2, 5)
    b = random.randint(1, 9)
    q_type = random.choice([1, 2])
    if q_type == 1:
      # (x + b)^2
      question = f"Khai triển biểu thức: $(x + {b})^2$"
      correct = f"x^2 + {2*b}x + {b**2}"
      wrongs = [
          f"x^2 + {b}x + {b**2}",
          f"x^2 + {2*b}x + {2*b}",
          f"x^2 - {2*b}x + {b**2}",
      ]
    else:
      # (a*x - b)(a*x + b)
      question = f"Thu gọn biểu thức: $({a}x - {b})({a}x + {b})$"
      correct = f"{a**2}x^2 - {b**2}"
      wrongs = [
          f"{a**2}x^2 + {b**2}",
          f"{a}x^2 - {b**2}",
          f"{a**2}x^2 - {2*b}",
      ]

  elif category == "DaThuc":
    # Phép nhân đơn thức với đa thức
    a = random.randint(2, 6)
    b = random.randint(2, 7)
    c = random.randint(1, 9)
    question = f"Rút gọn biểu thức: ${a}x({b}x - {c})$"
    correct = f"{a*b}x^2 - {a*c}x"
    wrongs = [
        f"{a*b}x^2 - {c}x",
        f"{a+b}x^2 - {a*c}x",
        f"{a*b}x - {a*c}x",
    ]

  elif category == "PhuongTrinh":
    # Giải phương trình bậc nhất 1 ẩn ax + b = c
    x_val = random.randint(1, 10)
    a = random.randint(2, 6)
    b = random.randint(1, 15)
    c = a * x_val + b
    question = f"Tìm $x$ biết: ${a}x + {b} = {c}$"
    correct = f"x = {x_val}"
    wrongs = [f"x = {x_val + 1}", f"x = {x_val - 1}", f"x = {x_val * 2}"]

  else:
    # Hình học: Định lý Pythagoras
    a = random.choice([3, 5, 6, 8, 9, 12])
    b = random.choice([4, 12, 8, 15, 12, 16])
    c_val = int((a**2 + b**2) ** 0.5)
    if a**2 + b**2 == c_val**2:
      question = (
          f"Cho $\\triangle ABC$ vuông tại $A$ có $AB = {a}\\text{{ cm}}$, $AC ="
          f" {b}\\text{{ cm}}$. Độ dài $BC$ là:"
      )
      correct = f"{c_val} cm"
      wrongs = [f"{c_val + 2} cm", f"{c_val - 1} cm", f"{a + b} cm"]
    else:
      question = "Trong một tam giác vuông, bình phương cạnh huyền bằng:"
      correct = "Tổng bình phương hai cạnh góc vuông"
      wrongs = [
          "Tích hai cạnh góc vuông",
          "Hiệu bình phương hai cạnh góc vuông",
          "Tổng hai cạnh góc vuông",
      ]

  options = [correct] + wrongs
  random.shuffle(options)
  return question, correct, options


# Khởi tạo trạng thái ứng dụng
if "score" not in st.session_state:
  st.session_state.score = 0
if "high_score" not in st.session_state:
  st.session_state.high_score = 0
if "current_q" not in st.session_state:
  st.session_state.current_q = generate_question()
if "game_over" not in st.session_state:
  st.session_state.game_over = False

# Giao diện chính
st.title("📐 Game Đấu Trí Toán Lớp 8")
st.write("Hãy kiểm tra kiến thức Toán 8 của bạn bằng cách trả lời các câu hỏi!")

# Hiển thị điểm số
col1, col2 = st.columns(2)
col1.metric("Điểm hiện tại", st.session_state.score)
col2.metric("Kỷ lục", st.session_state.high_score)

st.divider()

if not st.session_state.game_over:
  q_text, correct_ans, options = st.session_state.current_q

  st.subheader(q_text)

  # Form chọn đáp án
  with st.form(key="quiz_form"):
    user_choice = st.radio("Chọn đáp án đúng:", options)
    submit = st.form_submit_button("Nộp bài")

  if submit:
    if user_choice == correct_ans:
      st.success("🎉 Chính xác! Bạn được +10 điểm.")
      st.session_state.score += 10
      if st.session_state.score > st.session_state.high_score:
        st.session_state.high_score = st.session_state.score
      # Chuyển câu tiếp theo
      st.session_state.current_q = generate_question()
      time.sleep(1)
      st.rerun()
    else:
      st.error(f"❌ Sai rồi! Đáp án đúng là: **{correct_ans}**")
      st.session_state.game_over = True

else:
  st.warning("🎮 Game Over! Bạn đã chọn sai đáp án.")
  st.write(f"Tổng điểm của bạn là: **{st.session_state.score} điểm**")
  if st.button("Chơi lại từ đầu"):
    st.session_state.score = 0
    st.session_state.game_over = False
    st.session_state.current_q = generate_question()
    st.rerun()
