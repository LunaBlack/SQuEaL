
开发环境
-----------------
windows + python3.4
注：python2运行可能会出错


程序运行
-----------------
将三个py文件与需要处理的csv文件放在同一目录下
运行`squeal.py`  
在`Enter a SQuEaL query, or a blank line to exit:`后输入SQuEaL语句，等待屏幕输出结果
输出完成后，继续之前的循环，直至输入空行

如：
输入
select * from oscar-actor,oscar-film,books where a.year=f.year,a.title=f.title,book.year=a.year
输出
f.year,f.title,a.year,book.year,f.category,a.title,book.author,a.actor,book.title,a.category
1979,Kramer vs. Kramer,1979,1979,Directing,Kramer vs. Kramer,Douglas Hofstadter,Dustin Hoffman,Godel Escher Bach,Actor-Leading Role
1979,Kramer vs. Kramer,1979,1979,Best Picture,Kramer vs. Kramer,Douglas Hofstadter,Dustin Hoffman,Godel Escher Bach,Actor-Leading Role
1979,Kramer vs. Kramer,1979,1979,Directing,Kramer vs. Kramer,Douglas Hofstadter,Meryl Streep,Godel Escher Bach,Actress-Supporting Role
1979,Kramer vs. Kramer,1979,1979,Best Picture,Kramer vs. Kramer,Douglas Hofstadter,Meryl Streep,Godel Escher Bach,Actress-Supporting Role 


设计思路
-----------------
要求实现squeal语句查询。（有限的几种查询类型）
将当前目录下的csv数据视为数据库，输入squeal语句，输出数据库中对应查询结果。

database.py
定义类Table：
属性tdict，表对应的字典{列名: 值对应的list}
方法包括：根据指定文件名修改tdict(file_to_table)；
          根据指定Table修改tdict，即复制Table(table_to_table);
		  根据指定字典修改tdict(dict_to_table)
		  删除指定行(del_row)
		  删除指定列(del_col)
定义类Database：
属性dbdict，数据库对应的字典{表名称: 对应的Table对象}
方法包括：根据指定的文件列表修改dbdict(set_dbdict)

reading.py
两个函数分别生成Table对象和Database对象

squeal.py
num_rows：计算指定Table对象的数据行的行数
squeal_token：将squeal语句划分为各个token，返回其中的列名、表名、约束
cartesian_product：计算两个Table对象的笛卡尔积，返回对应的新Table对象
constraint_apply：根据指定的约束(参数包括约束中对应的列名/值和运算符)，返回需要删除的行
del_rows：根据约束删除一些行
del_cols：根据squeal语句(select)删除一些列
constraint_token：将指定的约束划分为各个token，包括运算符、列名、值
run_query：执行squeal语句
print_csv：打印出squeal语句的执行结果

运行逻辑：
1. 根据当前目录下的csv文件，生成Database对象
2. 用户输入squeal语句，传给run_query函数
3. squeal_token函数划分squeal语句，提取出其中的列名、表名、约束
4. 根据squeal语句中的表名，cartesian_product函数生成各表的笛卡尔积
5. 根据squeal语句中的约束，constraint_apply函数计算出需要删除的行，del_rows删除这些行
6. 根据squeal语句中的列名，del_cols函数删除未选中的列
7. 最终结果被返回给run_query函数，print_csv将结果打印出来
8. 重复运行步骤2-7，直至步骤2中输入空行


