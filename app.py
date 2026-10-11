import random
import time
import streamlit as st

# Cấu hình trang gọn gàng
st.set_page_config(
    page_title="Đấu Trí Toán 8", page_icon="📐", layout="centered"
)

# Giao diện CSS tùy chỉnh để làm đẹp form và nút bấm
st.markdown(
    """
    <style>
    .stButton>button {
        width: 100%;
        border-radius: 8px;
        font-weight: bold;
        height: 45px;
    }
    .stRadio>label {
        font-weight: 600;
        font-size: 16px;
    }
    </style>
""",
    unsafe_allow_html=True,
)


# Hàm tạo câu hỏi Toán lớp 8 tăng độ khó theo điểm
def generate_question(score):
  level = min(5, 1 + score // 30)
  category = random.choice([
      "HangDangThuc",
      "DaThuc",
      "PhuongTrinh",
      "HinhHoc",
  ])

  if category == "HangDangThuc":
    a = random.randint(1, level + 1)
    b = random.randint(2, 5 * level)
    q_type = random.choice([1, 2])
    if q_type == 1:
      question = f"Khai triển biểu thức: $(x + {b})^2$"
      correct = f"x^2 + {2*b}x + {b**2}"
      wrongs = [
          f"x^2 + {b}x + {b**2}",
          f"x^2 + {2*b}x + {2*b}",
          f"x^2 - {2*b}x + {b**2}",
      ]
    else:
      question = f"Thu gọn biểu thức: $({a}x - {b})({a}x + {b})$"
      correct = f"{a**2}x^2 - {b**2}"
      wrongs = [
          f"{a**2}x^2 + {b**2}",
          f"{a}x^2 - {b**2}",
          f"{a**2}x^2 - {2*b}",
      ]

  elif category == "DaThuc":
    a = random.randint(2, level + 2)
    b = random.randint(2, level + 3)
    c = random.randint(1, 5 * level)
    question = f"Rút gọn biểu thức: ${a}x({b}x - {c})$"
    correct = f"{a*b}x^2 - {a*c}x"
    wrongs = [
        f"{a*b}x^2 - {c}x",
        f"{a+b}x^2 - {a*c}x",
        f"{a*b}x - {a*c}x",
    ]

  elif category == "PhuongTrinh":
    x_val = random.randint(1, 5 * level)
    a = random.randint(2, level + 2)
    b = random.randint(1, 10 * level)
    c = a * x_val + b
    question = f"Tìm $x$ biết: ${a}x + {b} = {c}$"
    correct = f"x = {x_val}"
    wrongs = [f"x = {x_val + 1}", f"x = {x_val - 1}", f"x = {x_val * 2}"]

  else:
    triplets = [(3, 4, 5), (6, 8, 10), (5, 12, 13), (9, 12, 15), (8, 15, 17)]
    chosen = random.choice(triplets[: max(2, level + 1)])
    a, b, c_val = chosen[0], chosen[1], chosen[2]
    question = (
        f"Cho $\\triangle ABC$ vuông tại $A$ có $AB = {a}\\text{{ cm}}$,$AC ="
        f" {b}\\text{{ cm}}$. Độ dài cạnh huyền $BC$ là:"
    )
    correct = f"{c_val} cm"
    wrongs = [f"{c_val + 2} cm", f"{c_val - 1} cm", f"{a + b} cm"]

  options = [correct] + wrongs
  random.shuffle(options)
  return question, correct, options, level


# Khởi tạo trạng thái game
if "score" not in st.session_state:
  st.session_state.score = 0
if "high_score" not in st.session_state:
  st.session_state.high_score = 0
if "current_data" not in st.session_state:
  st.session_state.current_data = generate_question(st.session_state.score)
if "game_over" not in st.session_state:
  st.session_state.game_over = False
if "start_time" not in st.session_state:
  st.session_state.start_time = time.time()

# --- TIÊU ĐỀ GỌN GÀNG ---
st.title("📐 Đấu Trí Toán 8")
st.markdown("*Chinh phục toán học – Càng chơi càng khó!*")
st.divider()

# --- KHU VỰC HIỂN THỊ CHỈ SỐ (METRICS) ---
q_text, correct_ans, options, current_level = st.session_state.current_data

col1, col2, col3 = st.columns(3)
col1.metric("🏆 Điểm",

vel}")
col3.metric("Kỷ lục", st.session_state.high_score)

st.divider()

if not st.session_state.game_over:
  st.subheader(q_text)

  # Thời gian giới hạn giảm dần theo cấp độ (Lv1: 20s, Lv5: 10s)
  time_limit = max(10, 22 - (current_level * 2))
  st.info(f"⏱️ Thời gian suy nghĩ cho câu này: khoảng {time_limit} giây.")

  # Form chọn đáp án
  with st.form(key="quiz_form"):
    user_choice = st.radio("Chọn đáp án đúng:", options)
    submit = st.form_submit_button("Nộp bài")

  if submit:
    if user_choice == correct_ans:
      bonus_points = 10 * current_level
      st.success(
          f"🎉 Chính xác! Bạn nhận được +{bonus_points} điểm (Thưởng cấp"
          f" độ)."
      )
      st.session_state.score += bonus_points
      if st.session_state.score > st.session_state.high_score:
        st.session_state.high_score = st.session_state.score

      # Tạo câu hỏi mới với điểm số đã tăng
      st.session_state.current_data = generate_question(st.session_state.score)
      time.sleep(1)
      st.rerun()
    else:
      st.error(f"❌ Sai rồi! Đáp án đúng là: **{correct_ans}**")
      st.session_state.game_over = True

else:
  st.warning("🎮 Game Over! Bạn đã chọn sai đáp án.")
  st.write(f"Tổng số điểm bạn đạt được là: **{st.session_state.score} điểm**")
  if st.button("Chơi lại từ đầu"):
    st.session_state.score = 0
    st.session_state.game_over = False
    st.session_state.current_data = generate_question(st.session_state.score)
    st.rerun()
