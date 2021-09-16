import sys
import itertools
from PyQt5.QtWidgets import QWidget, QMessageBox, QApplication
from cal_ticket import Ui_Form


class TicketQWidget(QWidget, Ui_Form):
    """
    界面初始化
    """
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle('凑票')  # 设置窗口标题
        self.yes_pushButton.clicked.connect(self.use_tool)
        self.contact_pushButton.clicked.connect(self.contact_info)
        self.result_textEdit.setVisible(False)

    def contact_info(self):
        msg_box_obj = QMessageBox(QMessageBox.Information, '使用说明',
                                  '票额分割符统一使用中文或英文逗号，不能交叉使用;\n'
                                  '(总额-票额)的浮动范围指您能接受的差值，可以为负数;')
        msg_box_obj.addButton(self.tr('确认'), QMessageBox.YesRole)
        msg_box_obj.exec_()
        return 0

    def use_tool(self):
        tickets = self.input_lineEdit.text()
        total = self.total_lineEdit.text()
        sub_data = self.sub_lineEdit.text()
        try:
            if not tickets or not total:
                msg_box_obj = QMessageBox(QMessageBox.Critical, '参数异常', '票额或总额不能为空')
                msg_box_obj.addButton(self.tr('确认'), QMessageBox.YesRole)
                msg_box_obj.exec_()
                return 0

            tickets_list = tickets.split(",") if len(tickets.split(",")) > 1 else tickets.split("，")
            if len(tickets_list) == 1 or (len(tickets_list) == 2 and tickets_list[1] == ''):
                msg_box_obj = QMessageBox(QMessageBox.Critical, '参数异常', '票额需要用逗号(，或则 ,)分开并有2个以上的数值')
                msg_box_obj.addButton(self.tr('确认'), QMessageBox.YesRole)
                msg_box_obj.exec_()
                return 0

        except Exception as e:
            msg_box_obj = QMessageBox(QMessageBox.Critical, '参数异常', f'异常：{e}')
            msg_box_obj.addButton(self.tr('确认'), QMessageBox.YesRole)
            msg_box_obj.exec_()
            return 0

        try:
            if '' in tickets_list:
                tickets_list.remove('')
            tickets_list = list(map(lambda x: float(x), tickets_list))
            total = float(total)
            sub_data = float(sub_data) if sub_data else 0
        except Exception as e:
            msg_box_obj = QMessageBox(QMessageBox.Critical, '异常', '票额、总额、差额都必须是数值')
            msg_box_obj.addButton(self.tr('确认'), QMessageBox.YesRole)
            msg_box_obj.exec_()
            return 0

        try:
            res = list()
            combination = 0
            for i in range(1, len(tickets_list)+1):
                iter_ticket = itertools.combinations(tickets_list, i)
                for item in iter_ticket:
                    if sub_data >= 0 and total >= sum(item) >= total - sub_data:
                        combination += 1
                        info = (f'组合{str(combination)}的票额为：{str("%.2f"%(sum(item)))} ；'
                                f'总额-票额= {str("%.2f"%(total - sum(item)))}；'
                                f' 票额组合：{item}')
                        res.append(info)
                    elif sub_data < 0 and total+abs(sub_data) >= sum(item) >= total:
                        combination += 1
                        info = (f'组合{str(combination)}的票额为：{str("%.2f"%(sum(item)))} ；'
                                f'总额-票额= {str("%.2f"%(total - sum(item)))}； '
                                f'票额组合：{item}')
                        res.append(info)

            if len(res) == 0:
                text_info = (f'当前票额总数是：{str("%.2f"%(sum(tickets_list)))}'
                             f'  差额为：{str("%.2f"%(total-sum(tickets_list)))}'
                             f'\n没有差额范围为在 {str("%.2f"%sub_data)} 以内的符合要求的组合，请尝试修改差额')
            else:
                text_info = ''
                for info in res:
                    text_info += info + '\n'
            self.result_textEdit.setVisible(True)
            self.result_textEdit.setText(text_info)
            return 0
        except Exception as e:
            msg_box_obj = QMessageBox(QMessageBox.Critical, '异常', f'计算出错,异常{repr(e)}')
            msg_box_obj.addButton(self.tr('确认'), QMessageBox.YesRole)
            msg_box_obj.exec_()
            return 0


if __name__ == '__main__':
    app = QApplication(sys.argv)
    controller = TicketQWidget()
    controller.show()
    sys.exit(app.exec_())

# pyinstaller -F -w -p D:\AprogramData\Miniconda3\envs\py3.8_offline_tool_gui_template\Lib\site-packages -i D:\myproject_fromgit\offline_tool_gui_template\PyQt\resources\favicon.ico cal_ticket_window.py
