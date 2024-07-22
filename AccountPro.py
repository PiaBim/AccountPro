import random

FILE_PATH = "accounts.txt"

class AccountManager:
    def __init__(self):
        self.accArr = []

    # 랜덤한 고유 ID 생성 함수
    def generate_unique_id(self):
        while True:
            new_id = random.randint(1000, 9999)
            if not any(acc['uniqueID'] == new_id for acc in self.accArr):
                return new_id

    # 계좌를 생성하는 함수
    def make_account(self):
        print("[계좌개설]")
        newAcc = {}

        # 새로운 계좌 ID 할당
        while True:
            try:
                newAcc['accID'] = int(input("계좌ID (취소하려면 -1 입력): "))
                if newAcc['accID'] == -1:
                    print("계좌 개설을 취소합니다.")
                    return
            except ValueError:
                print("올바른 숫자를 입력하세요.")
                continue
            if any(acc['accID'] == newAcc['accID'] for acc in self.accArr):
                print("이미 존재하는 계좌ID입니다. 다시 입력해주세요.")
            else:
                break

        # 고유 ID 생성
        newAcc['uniqueID'] = self.generate_unique_id()

        while True:
                newAcc['accName'] = input("이름:")
                if newAcc['accName'].isalpha():
                    break
                else:
                    print("문자만 입력하세요.")
                    continue
        
        while True:
            try:
                newAcc['balance'] = int(input("입금액: "))
                break
            except ValueError:
                print("올바른 숫자를 입력하세요.")

        self.accArr.append(newAcc)

        with open(FILE_PATH, "a") as file:
            file.write(f"{newAcc['accID']} {newAcc['accName']} {newAcc['balance']} {newAcc['uniqueID']}\n")

    # 입금하는 함수
    def deposit_money(self):
        print("[입 금]")
        try:
            accID = int(input("계좌ID: "))
        except ValueError:
            print("올바른 숫자를 입력하세요.")
            return

        account = next((acc for acc in self.accArr if acc['accID'] == accID), None)
        if account is None:
            print("계좌 ID가 존재하지 않습니다.")
            return
        try:
            amount = int(input("입금액: "))
        except ValueError:
            print("올바른 숫자를 입력하세요.")
            return
        
        account['balance'] += amount
        print(f"입금이 완료되었습니다. 현재 잔액: {account['balance']}")
    # 출금하는 함수
    def withdraw_money(self):
        print("[출 금]")
        try:
            accID=int(input("계좌ID:"))
        except ValueError:
            print("올바른 숫자를 입력하세요.")
            return
        account=next((acc for acc in self.accArr if acc['accID']==accID),None)
        if account is None:
            print("계좌가 존재하지 않습니다.")
        try:
            amount=int(input("출금액:"))
        except:
            print("올바른 숫자를 입력하세요.")
            return
        
        if account['balance']>=amount:
            account['balance']-=amount
            print(f"출금이 완료되었습니다. 현재 잔액:{account['balance']}")
        else:
            print("잔액이 부족합니다.")
            return
    # 모든 계좌 정보를 출력하는 함수
    def show_all_acc_info(self):
        if not self.accArr:
            print("등록된 계좌가 없습니다.")
        else:
            print("[계좌정보 전체 출력]")
            for acc in self.accArr:
                print(f"계좌ID: {acc['accID']} 이름: {acc['accName']} 잔액: {acc['balance']} 고유ID: {acc['uniqueID']}")

    # 계좌를 삭제하는 함수
    def delete_account(self):
        accID = int(input("[계좌삭제]\n삭제할 계좌ID: "))

        for idx, acc in enumerate(self.accArr):
            if acc['accID'] == accID:
                del self.accArr[idx]
                print("계좌 삭제 완료")
                return

        print("해당 계좌ID가 존재하지 않습니다.")

    # 프로그램 시작 시 계좌 정보를 파일에서 읽어오는 함수
    def load_accounts(self):
        try:
            with open(FILE_PATH, "r") as file:
                for line in file:
                    accID, accName, balance, uniqueID = line.strip().split()
                    self.accArr.append({
                        'accID': int(accID),
                        'accName': accName,
                        'balance': int(balance),
                        'uniqueID': int(uniqueID)
                    })
        except FileNotFoundError:
            pass

    # 프로그램 종료 시 계좌 정보를 파일에 저장하는 함수
    def save_accounts(self):
        with open(FILE_PATH, "w") as file:
            for acc in self.accArr:
                file.write(f"{acc['accID']} {acc['accName']} {acc['balance']} {acc['uniqueID']}\n")

    # 메뉴를 출력하는 함수
    def show_menu(self):
        print("----Menu----")
        print("1. 계좌개설")
        print("2. 입 금")
        print("3. 출 금")
        print("4. 계좌정보 전체 출력")
        print("5. 계좌삭제")
        print("9. 프로그램 종료")

if __name__ == "__main__":
    manager = AccountManager()
    manager.load_accounts()

    while True:
        manager.show_menu()
        try:
            choice = int(input("선택: "))
        except ValueError:
            print("잘못된 입력입니다. 다시 선택해주세요.")
            continue

        if choice == 1:
            manager.make_account()
        elif choice == 2:
            manager.deposit_money()
        elif choice == 3:
            manager.withdraw_money()
        elif choice == 4:
            manager.show_all_acc_info()
        elif choice == 5:
            manager.delete_account()
        elif choice == 9:
            manager.save_accounts()
            break
        else:
            print("잘못된 입력입니다. 다시 선택해주세요.")
