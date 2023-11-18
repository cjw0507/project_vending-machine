import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import cv2
from PIL import Image, ImageTk
import random
import requests
from twilio.rest import Client
import datetime

datetime.datetime.today()
datetime.datetime.now()
now= datetime.datetime.now()
time=now.strftime('%Y-%m-%d %H:%M:%S')



account_sid = 'ACe2f3e8e78588f56215685a716e75d222'
auth_token = '6b900baf93ab57d1e8ba6c983f6b647f'
client = Client(account_sid, auth_token)
class ChineseRestaurantApp:
    def __init__(self, root):
        self.root = root
        self.root.title("중국집 키오스크")

        self.balance = 50000  # 초기 잔액 설정

        self.food_menu = {
            "짜장면(5000원)": {"price": 5000, "quantity":(1)},
            "짬뽕(6000원)": {"price": 6000, "quantity": (1)},
            "탕수육(12000원)": {"price": 12000, "quantity": (1)},
            "볶음밥(7000원)": {"price": 7000, "quantity": (1)},
            "우동(5500원)": {"price": 5500, "quantity": (1)},
            "냉면(6000원)": {"price": 6000, "quantity": (1)},
            "깐풍기(14000원)": {"price": 14000, "quantity": (1)},
            "잡채밥(8000원)": {"price": 8000, "quantity": (1)}
        }

        self.drink_menu = {
            "콜라(2000원)": {"price": 2000, "quantity": (1)},
            "사이다(2000원)": {"price": 2000, "quantity":(1)},
            "녹차(2500원)": {"price": 2500, "quantity": (1)},
            "커피(2500원)": {"price": 2500, "quantity": (1)}
        }

        self.food_menu_initial_quantity = {item: self.food_menu[item]["quantity"] for item in self.food_menu}
        self.drink_menu_initial_quantity = {item: self.drink_menu[item]["quantity"] for item in self.drink_menu}

        self.order = {item: 0 for item in self.food_menu}
        self.current_menu = self.food_menu

        self.food_images = {
            "짜장면(5000원)": "짜장면.png",  # 이미지 파일 이름을 적절히 변경해야 합니다.
            "짬뽕(6000원)": "짬뽕.png",
            "탕수육(12000원)": "탕수육.png",
            "볶음밥(7000원)": "볶음밥.png",
            "우동(5500원)": "우동.png",
            "냉면(6000원)": "냉면.png",
            "깐풍기(14000원)": "깐풍기.png",
            "잡채밥(8000원)": "잡채밥.png"
        }
        self.drink_images = {
            "콜라(2000원)": "콜라.png",  # 이미지 파일 이름을 적절히 변경해야 합니다.
            "사이다(2000원)": "사이다.png",
            "녹차(2500원)": "녹차.png",
            "커피(2500원)": "커피.png"
        }

        self.create_widgets()

        self.order_history = {}

    def create_widgets(self):
        self.balance_label = tk.Label(self.root, text=f"잔액: {self.balance}원", font=("Helvetica", 14))
        self.balance_label.grid(row=0, column=0, padx=10, pady=10, sticky="nw")

        self.charge_button = tk.Button(self.root, text="잔액 충전", command=self.scan_qr_code)
        self.charge_button.grid(row=0, column=1, padx=10, pady=10, sticky="ne")

        self.tab_control = ttk.Notebook(self.root)
        self.tab_food = ttk.Frame(self.tab_control)
        self.tab_drink = ttk.Frame(self.tab_control)
        self.tab_control.add(self.tab_food, text="음식 메뉴")
        self.tab_control.add(self.tab_drink, text="음료 메뉴")
        self.tab_control.grid(row=1, column=0, columnspan=2, padx=10, pady=10, sticky="nsew")

        self.menu_buttons_food = {}
        self.menu_buttons_drink = {}

        food_frame = ttk.Frame(self.tab_food)
        food_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        food_index = 0
        row_index = 0
        for item, details in self.food_menu.items():
            frame = ttk.Frame(food_frame)
            frame.grid(row=row_index, column=food_index % 4, padx=10, pady=10)

            btn_text = f"{item}"
            button = tk.Button(frame, text=btn_text, command=lambda i=item: self.buy_item(i, menu_type="food"))
            button.pack()

            if item in self.food_images:
                image_path = self.food_images[item]
                image = Image.open(image_path)
                image = image.resize((100, 100), Image.LANCZOS)
                photo = ImageTk.PhotoImage(image)
                image_label = tk.Label(frame, image=photo)
                image_label.image = photo
                image_label.pack()

            food_index += 1
            if food_index % 4 == 0:
                row_index += 1

        drink_frame = ttk.Frame(self.tab_drink)
        drink_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)  # 프레임에 패딩을 추가하여 간격을 조정합니다.

        drink_index = 0
        row_index = 0
        for item, details in self.drink_menu.items():
            frame = ttk.Frame(drink_frame)  # 각 항목마다 프레임을 생성합니다.
            frame.grid(row=row_index, column=drink_index % 4, padx=10, pady=10)  # 각 프레임의 위치를 설정합니다.

            btn_text = f"{item}"
            button = tk.Button(frame, text=btn_text, command=lambda i=item: self.buy_item(i, menu_type="drink"))
            button.pack()

            if item in self.drink_images:
                image_path = self.drink_images[item]
                image = Image.open(image_path)
                image = image.resize((100, 100), Image.LANCZOS)
                photo = ImageTk.PhotoImage(image)
                image_label = tk.Label(frame, image=photo)
                image_label.image = photo
                image_label.pack()

            drink_index += 1
            if drink_index % 4 == 0:
                row_index += 1
        self.order_frame = tk.Frame(self.root)
        self.order_frame.grid(row=2, column=0, columnspan=2, padx=10, pady=10, sticky="nsew")

        self.order_textbox = tk.Text(self.order_frame, height=10, width=40)
        self.order_textbox.grid(row=0, column=0, padx=10, pady=10)

        self.clear_order_button = tk.Button(self.order_frame, text="주문 내역 초기화", command=self.clear_order)
        self.clear_order_button.grid(row=1, column=0, padx=10, pady=10)

        self.checkout_button = tk.Button(self.root, text="주문 결제", command=self.checkout, width=20, height=2)
        self.checkout_button.grid(row=3, column=1, padx=10, pady=10, sticky="se")

    def update_menu_buttons(self):
        food_frame = ttk.Frame(self.tab_food)
        food_frame.pack()
        drink_frame = ttk.Frame(self.tab_drink)
        drink_frame.pack()

        for btn in self.menu_buttons_food.values():
            btn.destroy()

        for item in self.food_menu:
            btn_text = f"{item} ({self.food_menu[item]['quantity']}개 남음)"
            btn = tk.Button(food_frame, text=btn_text, command=lambda i=item: self.buy_item(i, menu_type="food"))
            btn.pack(side=tk.LEFT, padx=10, pady=5)

            if item in self.food_images:
                image_path = self.food_images[item]
                image = Image.open(image_path)
                image = image.resize((100, 100), Image.LANCZOS)
                photo = ImageTk.PhotoImage(image)
                image_label = tk.Label(food_frame, image=photo)
                image_label.image = photo
                image_label.pack(side=tk.LEFT)

            self.menu_buttons_food[item] = btn

        for btn in self.menu_buttons_drink.values():
            btn.destroy()

        for item in self.drink_menu:
            btn_text = f"{item} ({self.drink_menu[item]['quantity']}개 남음)"
            btn = tk.Button(drink_frame, text=btn_text, command=lambda i=item: self.buy_item(i, menu_type="drink"))
            btn.pack(side=tk.LEFT, padx=10, pady=5)

            if item in self.drink_images:
                image_path = self.drink_images[item]
                image = Image.open(image_path)
                image = image.resize((100, 100), Image.LANCZOS)
                photo = ImageTk.PhotoImage(image)
                image_label = tk.Label(drink_frame, image=photo)
                image_label.image = photo
                image_label.pack(side=tk.LEFT)

            self.menu_buttons_drink[item] = btn

        self.root.update()

    def buy_item(self, item, menu_type):
        if menu_type == "food":
            current_menu = self.food_menu
        elif menu_type == "drink":
            current_menu = self.drink_menu
        else:
            current_menu = None

        if current_menu is not None:
            if item in current_menu:
                if self.balance >= 0:
                    if item not in self.order:
                        self.order[item] = 0
                    self.order[item] += 1
                    current_menu[item]["quantity"] -= 1
                    self.update_button_text(item)
                    total_price = current_menu[item]["price"]
                    messagebox.showinfo("주문 완료", f"{item} 주문내역에 추가되었습니다\n가격: {total_price}원")
                    self.update_balance_label()
                    self.update_order_textbox()
                else:
                    messagebox.showinfo("잔액 부족", "잔액이 부족합니다.")
            else:
                messagebox.showinfo("주문 불가", "해당 메뉴는 현재 탭에서 주문할 수 없거나 존재하지 않습니다.")
        else:
            messagebox.showinfo("주문 불가", "해당 메뉴는 현재 탭에서 주문할 수 없거나 존재하지 않습니다.")

    def update_button_text(self, item):
        if item in self.menu_buttons_food:
            btn_text = f"{item} ({self.food_menu[item]['quantity']}개 남음)"
            self.menu_buttons_food[item].config(text=btn_text)
        elif item in self.menu_buttons_drink:
            btn_text = f"{item} ({self.drink_menu[item]['quantity']}개 남음)"
            self.menu_buttons_drink[item].config(text=btn_text)

    def update_balance_label(self):
        self.balance_label.config(text=f"잔액: {self.balance}원")



    def clear_order(self):
        for item in self.order:
            if item in self.food_menu:
                self.food_menu[item]["quantity"] += self.order[item]
        self.order = {item: 0 for item in self.food_menu}

        for item in self.food_menu:
            self.food_menu[item]["quantity"] = self.food_menu_initial_quantity[item]


        self.order_textbox.delete(1.0, tk.END)
        self.update_order_textbox()

        for item in self.menu_buttons_food:
            btn_text = f"{item} ({self.food_menu[item]['quantity']}개 남음)"
            self.menu_buttons_food[item].config(text=btn_text)

        messagebox.showinfo("주문 내역 초기화", "주문 내역이 초기"
                                         "화되었습니다.")

    def calculate_total_cost(self):
        food_cost = sum(
            self.food_menu[item]["price"] * self.order[item] for item in self.order if item in self.food_menu)
        drink_cost = sum(
            self.drink_menu[item]["price"] * self.order[item] for item in self.order if item in self.drink_menu)
        total_cost = food_cost + drink_cost
        return total_cost

    def checkout(self):


        global menupick

        food_cost = sum(
            self.food_menu[item]["price"] * self.order[item] for item in self.order if item in self.food_menu)
        drink_cost = sum(
            self.drink_menu[item]["price"] * self.order[item] for item in self.order if item in self.drink_menu)

        total_cost = food_cost + drink_cost

        if total_cost > 0:
            confirm_checkout = messagebox.askyesno("주문 결제", f"총 가격: {total_cost}원\n결제하시겠습니까?")

            if confirm_checkout:
                confirm_checkout = messagebox.askyesno("결제 방식 선택",
                                                       "결제 방식을 선택하세요.\n 예　　, 잔액으로 결제합니다.\n 아니요, 신용카드로 결제합니다.")
                if confirm_checkout:
                    if self.balance >= total_cost:
                        self.balance -= total_cost
                        self.update_balance_label()
                        ordered_items = [f"{item} x {quantity}" for item, quantity in self.order.items() if
                                         quantity > 0]
                        ordered_items_text = "\n".join(ordered_items)
                        for item in self.order:
                            self.order_history[item] = self.order_history.get(item, 0) + self.order[item]
                            menupick = self.order_history[item]
                            self.order[item] = 0
                        receipt_prompt = messagebox.askyesno("전자 영수증 발송", "결제 후 전자 영수증을 보내시겠습니까?")
                        if receipt_prompt:
                            message = client.messages.create(
                                to="+821086490456",
                                from_="+12053362123",
                                body="결제수단:잔액\n"f"\n주문일시:{time,}"f"\n주문 내역:\n{ordered_items_text}\n총 가격: {total_cost}원")
                            pass  # '아니요'를 선택한 경우 이 부분은 비워두세요
                        else:
                            pass  # 요청에 따라 이 부분은 비워두세요
                        messagebox.showinfo("주문 완료", "주문이 완료되었습니다. 맛있게 드세요!")
                        self.update_order_textbox()
                    else:
                        messagebox.showinfo("잔액 부족", "잔액이 부족합니다. 결제를 진행할 수 없습니다.")
                else:
                    cap = cv2.VideoCapture(0)
                    while True:
                        ret, frame = cap.read()
                        if not ret:
                            continue
                        qr_decoder = cv2.QRCodeDetector()
                        retval, decoded_info, _, _ = qr_decoder.detectAndDecodeMulti(frame)
                        if retval:
                            qr_data = decoded_info[0][0]
                            if (qr_data) == '신':
                                messagebox.showinfo("스캔 성공", "QR 코드 스캔이 완료되었습니다.")
                                ordered_items = [f"{item} x {quantity}" for item, quantity in self.order.items() if
                                                 quantity > 0]
                                ordered_items_text = "\n".join(ordered_items)
                                for item in self.order:
                                    self.order_history[item] = self.order_history.get(item, 0) + self.order[item]
                                    self.order[item] = 0

                                receipt_prompt = messagebox.askyesno("전자 영수증 발송", "결제 후 전자 영수증을 보내시겠습니까?")
                                if receipt_prompt:
                                    message = client.messages.create(
                                        to="+821086490456",
                                        from_="+12053362123",
                                        body="결제수단:신용카드\n"f"\n주문일시:{time,}"f"\n주문 내역:\n{ordered_items_text}\n총 가격: {total_cost}원")
                                    pass  # '아니요'를 선택한 경우 이 부분은 비워두세요
                                messagebox.showinfo("주문 완료", "주문이 완료되었습니다. 맛있게 드세요!")
                                self.update_order_textbox()
                                break

                            else:
                                messagebox.showinfo("스캔 실패", "올바르지 않은 QR 코드입니다.")
                        cv2.imshow("QR Code Scanner", frame)

                        if cv2.waitKey(1) & 0xFF == ord('q'):
                            break
                    cap.release()
                    cv2.destroyAllWindows()
        else:
            messagebox.showinfo("주문 내역 없음", "주문 내역이 비어 있습니다. 주문 후 결제해주세요.")

    def scan_qr_code(self):
        cap = cv2.VideoCapture(0)
        while True:
            ret, frame = cap.read()
            if not ret:
                continue

            qr_decoder = cv2.QRCodeDetector()
            retval, decoded_info, _, _ = qr_decoder.detectAndDecodeMulti(frame)
            if retval:
                qr_data = decoded_info[0][0]
                if int(str(decoded_info).replace("(", "").replace("'", "").replace(",", "").replace(")",
                                                                                                    "")) == 10000:
                    self.charge_balance(10000)
                    messagebox.showinfo("스캔 성공", "QR 코드 스캔이 완료되었습니다.")
                else:
                    messagebox.showinfo("스캔 실패", "올바르지 않은 QR 코드입니다.")
                break

            cv2.imshow("QR Code Scanner", frame)

            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

        cap.release()
        cv2.destroyAllWindows()

    def charge_balance(self, amount):
        if amount > 0:
            self.balance += amount
            self.update_balance_label()
            messagebox.showinfo("잔액 충전", f"{amount}원이 충전되었습니다.")
        else:
            messagebox.showinfo("잘못된 QR 코드", "유효하지 않은 QR 코드입니다.")

    def update_order_textbox(self):
        # 주문 내역을 텍스트 박스에 업데이트합니다.
        self.order_textbox.delete(1.0, tk.END)
        for item, quantity in self.order.items():
            if quantity > 0:
                order_summary = f"{item} x {quantity}\n"
                remove_button = tk.Button(self.order_textbox, text="X", command=lambda i=item: self.remove_order_item(i))
                self.order_textbox.window_create(tk.END, window=remove_button)
                self.order_textbox.insert(tk.END, order_summary)

    def remove_order_item(self, item):
        if item in self.order and self.order[item] > 0:
            if item in self.food_menu:
                self.food_menu[item]["quantity"] += 1
            elif item in self.drink_menu:
                self.drink_menu[item]["quantity"] += 1
            self.order[item] -= 1
            self.update_button_text(item)
            self.update_balance_label()
            self.update_order_textbox()

if __name__ == "__main__":
    root = tk.Tk()
    app = ChineseRestaurantApp(root)
    root.mainloop()