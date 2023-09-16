import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import cv2
import random


class ChineseRestaurantApp:
    def __init__(self, root):
        self.root = root
        self.root.title("중국집 자판기")

        self.balance = 50000  # 초기 잔액 설정

        self.food_menu = {
            "짜장면(5000원)": {"price": 5000, "quantity": random.randint(3, 10)},
            "짬뽕(6000원)": {"price": 6000, "quantity": random.randint(3, 10)},
            "탕수육(12000원)": {"price": 12000, "quantity": random.randint(3, 10)},
            "볶음밥(7000원)": {"price": 7000, "quantity": random.randint(3, 10)}
        }

        self.drink_menu = {
            "콜라(2000원)": {"price": 2000, "quantity": random.randint(3, 10)},
            "사이다(2000원)": {"price": 2000, "quantity": random.randint(3, 10)},
            "녹차(2500원)": {"price": 2500, "quantity": random.randint(3, 10)},
            "커피(2500원)": {"price": 2500, "quantity": random.randint(3, 10)}
        }

        self.food_menu_initial_quantity = {item: self.food_menu[item]["quantity"] for item in self.food_menu}
        self.drink_menu_initial_quantity = {item: self.drink_menu[item]["quantity"] for item in self.drink_menu}

        self.order = {item: 0 for item in self.food_menu}
        self.current_menu = self.food_menu

        self.create_widgets()

    def create_widgets(self):
        self.balance_label = tk.Label(self.root, text=f"잔액: {self.balance}원", font=("Helvetica", 14))
        self.balance_label.pack(pady=10)

        self.charge_button = tk.Button(self.root, text="잔액 충전", command=self.scan_qr_code)
        self.charge_button.pack(pady=10)

        self.tab_control = ttk.Notebook(self.root)
        self.tab_food = ttk.Frame(self.tab_control)
        self.tab_drink = ttk.Frame(self.tab_control)
        self.tab_control.add(self.tab_food, text="음식 메뉴")
        self.tab_control.add(self.tab_drink, text="음료 메뉴")
        self.tab_control.pack(padx=30, pady=30)

        self.menu_buttons_food = {}
        self.menu_buttons_drink = {}

        self.update_menu_buttons()

        # 주문 내역 확인 버튼
        self.view_order_button = tk.Button(self.root, text="주문 내역 확인", command=self.view_order)
        self.view_order_button.pack(pady=10)

        # 주문 내역 초기화 버튼
        self.clear_order_button = tk.Button(self.root, text="주문 내역 초기화", command=self.clear_order)
        self.clear_order_button.pack(pady=10)

        # 주문 기록
        self.order_history = {}

        # 결제 버튼
        self.checkout_button = tk.Button(self.root, text="주문 결제", command=self.checkout)
        self.checkout_button.pack(pady=10)

    def update_menu_buttons(self):

        for btn in self.menu_buttons_food.values():
            btn.destroy()

        for item in self.food_menu:
            btn_text = f"{item} ({self.food_menu[item]['quantity']}개 남음)"
            btn = tk.Button(self.tab_food, text=btn_text, command=lambda i=item: self.buy_item(i, menu_type="food"))
            btn.pack(padx=10, pady=5)
            self.menu_buttons_food[item] = btn


        for btn in self.menu_buttons_drink.values():
            btn.destroy()

        for item in self.drink_menu:
            btn_text = f"{item} ({self.drink_menu[item]['quantity']}개 남음)"
            btn = tk.Button(self.tab_drink, text=btn_text, command=lambda i=item: self.buy_item(i, menu_type="drink"))
            btn.pack(padx=10, pady=5)
            self.menu_buttons_drink[item] = btn

    def buy_item(self, item, menu_type):
        if menu_type == "food":
            current_menu = self.food_menu
        elif menu_type == "drink":
            current_menu = self.drink_menu
        else:
            current_menu = None

        if current_menu is not None:
            if item in current_menu and current_menu[item]["quantity"] > 0:
                if self.balance >= 0:
                    if item not in self.order:
                        self.order[item] = 0
                    self.order[item] += 1
                    current_menu[item]["quantity"] -= 1
                    self.update_button_text(item)
                    total_price = current_menu[item]["price"]
                    messagebox.showinfo("주문 완료", f"{item} 주문내역에 추가되었습니다\n가격: {total_price}원")
                    self.update_balance_label()
                else:
                    messagebox.showinfo("잔액 부족", "잔액이 부족합니다.")
            elif item in current_menu and current_menu[item]["quantity"] <= 0:
                messagebox.showinfo("품절", f"{item}은(는) 품절되었습니다.")
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

    def view_order_history(self):
        order_summary = "주문 기록:\n"
        for item, quantity in self.order_history.items():
            if quantity > 0:
                order_summary += f"{item} x {quantity}\n"
        if order_summary == "주문 기록:\n":
            order_summary += "주문 기록이 없습니다."
        messagebox.showinfo("주문 기록", order_summary)

    def view_order(self):
        order_summary = "주문 내역:\n"
        for item, quantity in self.order.items():
            if quantity > 0:
                order_summary += f"{item} x {quantity}\n"
        if order_summary == "주문 내역:\n":
            order_summary += "주문 내역이 비어 있습니다."
        messagebox.showinfo("주문 내역", order_summary)

    def clear_order(self):
        for item in self.order:
            if item in self.food_menu:
                self.food_menu[item]["quantity"] += self.order[item]
            elif item in self.drink_menu:
                self.drink_menu[item]["quantity"] += self.order[item]
        self.order = {item: 0 for item in self.food_menu}
        self.update_menu_buttons()
        messagebox.showinfo("주문 내역 초기화", "주문 내역이 초기화되었습니다.")

    def checkout(self):
        food_cost = sum(
            self.food_menu[item]["price"] * self.order[item] for item in self.order if item in self.food_menu)
        drink_cost = sum(
            self.drink_menu[item]["price"] * self.order[item] for item in self.order if item in self.drink_menu)

        total_cost = food_cost + drink_cost

        if total_cost > 0:

            confirm_checkout = messagebox.askyesno("주문 결제", f"총 가격: {total_cost}원\n결제하시겠습니까?")


            if confirm_checkout:
                confirm_checkout = messagebox.askyesno("결제 방식 선택", "잔액으로 결제하시겠습니까?,아니요를 누르면 신용카드결제로 넘어갑니다")
                if confirm_checkout:
                    if self.balance >= total_cost:
                        self.balance -= total_cost
                        self.update_balance_label()
                        for item in self.order:
                            self.order_history[item] = self.order_history.get(item, 0) + self.order[item]
                            self.order[item] = 0
                        messagebox.showinfo("주문 완료", "주문이 완료되었습니다. 맛있게 드세요!")
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
                                for item in self.order:
                                    self.order_history[item] = self.order_history.get(item, 0) + self.order[item]
                                    self.order[item] = 0
                                messagebox.showinfo("주문 완료", "주문이 완료되었습니다. 맛있게 드세요!")
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


if __name__ == "__main__":
    root = tk.Tk()
    app = ChineseRestaurantApp(root)
    root.mainloop()
