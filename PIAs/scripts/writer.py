import xlsxwriter


class TSV():

    def __init__(self,file_name):

        # Create a workbook and add a self.worksheet.
        self.path      = ('TSV_FILES/PIAtest/'+file_name+".xlsx")
        self.workbook  = xlsxwriter.Workbook(self.path) #object store path?
        self.worksheet = self.workbook.add_worksheet()

    def file(self,ri):

        # Start from the first cell. Rows and columns are zero indexed.
        self.worksheet.write(0, 0,'app')
        self.worksheet.write(0, 1,'family')
        self.worksheet.write(0, 2,'threat')
        self.worksheet.write(0, 3,'likely')
        self.worksheet.write(0, 4,'step')
        self.worksheet.write(0, 5,'D=en:A')
        self.worksheet.write(0, 6,'D=en:I')
        self.worksheet.write(0, 7,'D=en:C')
        self.worksheet.write(0, 8,'D=en:Auth')
        self.worksheet.write(0, 9,'D=en:Acc')
        self.worksheet.write(0, 10,'D=en:V')
        self.worksheet.write(0, 11,'D=en:PD')
        self.worksheet.write(1, 0,'no')
        self.worksheet.write(1, 5,'availability')
        self.worksheet.write(1, 6,'integrity')
        self.worksheet.write(1, 7,'confidentiality')
        self.worksheet.write(1, 8,'authenticity')
        self.worksheet.write(1, 9,'accountability')
        self.worksheet.write(1, 10,'value')
        self.worksheet.write(1, 11,'personal data')
        row_index=0
        for r in ri:
            self.worksheet.write(2+row_index, 1,r['Family'])
            self.worksheet.write(2+row_index, 2,r['Thread'])
            self.worksheet.write(2+row_index, 3,r['likely'])
            percent_fmt = self.workbook.add_format({'num_format': '0%'})
            self.worksheet.write(2+row_index, 5, r['A'], percent_fmt)
            self.worksheet.write(2+row_index, 6, r['I'], percent_fmt)
            self.worksheet.write(2+row_index, 7, r['C'], percent_fmt)
            self.worksheet.write(2+row_index, 8, r['Auth'], percent_fmt)
            row_index+=1

        self.workbook.close()
        return self.path

# Iterate over the data and write it out row by row.

# Write a total using a formula.
if __name__ == '__main__':
    ri=[{'Family':"random",'Thread':"thread", 'likely':10,
                        'A': 20, 'I':30, 'C': 40,
                        'Auth':50},{'Family':"random2",'Thread':"thread", 'likely':10,
                        'A': 30, 'I':30, 'C': 40,
                        'Auth':50}]
    a=TSV().file(ri)
    print (a)


