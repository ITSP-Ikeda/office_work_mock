import win32com.client

print("月次処理開始")

xl = win32com.client.GetObject(Class="Excel.Application")

year  = xl.sheets("支払いテンプレート").Range("H2").Value
month = xl.sheets("支払いテンプレート").Range("H4").Value

# https://office54.net/python/excel/python-excel-lasthistory_row
xlUp = -4162
history_row = xl.sheets("駐車場使用履歴").Cells(10000, 1).End(xlUp).Row
payment_row = xl.sheets("月次支払い").Cells(10000, 1).End(xlUp).Row

for i in range(5, 25):
	print("支払いテンプレート：" + str(i) + "行目処理中")
	if xl.sheets("支払いテンプレート").Cells(i, 1).value is not None and xl.sheets("支払いテンプレート").Cells(i, 2).value is not None:
		history_row = history_row + 1
		xl.sheets("駐車場使用履歴").Cells(history_row, 1).Value = year
		xl.sheets("駐車場使用履歴").Cells(history_row, 2).Value = month
		xl.sheets("駐車場使用履歴").Cells(history_row, 3).Value = xl.sheets("支払いテンプレート").Cells(i, 1)
		xl.sheets("駐車場使用履歴").Cells(history_row, 4).Value = xl.sheets("支払いテンプレート").Cells(i, 2)
		xl.sheets("駐車場使用履歴").Cells(history_row, 5).Value = xl.sheets("支払いテンプレート").Cells(i, 3)
		xl.sheets("駐車場使用履歴").Cells(history_row, 6).Value = "=VLOOKUP(C" + str(history_row) + ",駐車場区画マスタ!$A$2:$B$1048576,2,)"
		xl.sheets("駐車場使用履歴").Cells(history_row, 7).Value = "=VLOOKUP(F" + str(history_row) + ",駐車場マスタ!$A$2:$B$1048576,2,)"
		xl.sheets("駐車場使用履歴").Cells(history_row, 8).Value = "=A" + str(history_row) + "&RIGHT(\"0\"&B" + str(history_row) + ",2)&G" + str(history_row)
		xl.sheets("駐車場使用履歴").Cells(history_row, 9).Value = xl.sheets("支払いテンプレート").Cells(i, 4)
		
		flg = ""
		for j in range(2, payment_row + 1):
			if xl.sheets("月次支払い").Cells(j, 1).Value == year and xl.sheets("月次支払い").Cells(j, 2).Value == month and xl.sheets("月次支払い").Cells(j, 3).Value == xl.sheets("支払いテンプレート").Cells(i, 6).Value:
				flg = 1

		if flg == "":
			payment_row += 1 
			xl.sheets("月次支払い").Cells(payment_row, 1).Value = year
			xl.sheets("月次支払い").Cells(payment_row, 2).Value = month
			xl.sheets("月次支払い").Cells(payment_row, 3).Value = xl.sheets("支払いテンプレート").Cells(i, 6).Value
			xl.sheets("月次支払い").Cells(payment_row, 4).Value = "=VLOOKUP(C" + str(payment_row) + ",支払い先マスタ!$A$2:$B$1048576,2,)"
			xl.sheets("月次支払い").Cells(payment_row, 5).Value = "=SUMIF(駐車場使用履歴!$H:$H,F" + str(payment_row) + ",駐車場使用履歴!$I:$I)"
			xl.sheets("月次支払い").Cells(payment_row, 6).Value = "=A" + str(payment_row) + "&RIGHT(\"0\"&B" + str(payment_row) + ",2)&C" + str(payment_row)
print("月次処理終了")
