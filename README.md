# RELE-GL针对于规则的文本过滤

# 缘由

对于我遇到的情况来说，比如攻防的时候遇到了批量的IP有需求就当时简单的脚本处理下，事后脚本就扔了，下次在用了就一直重复....。还有就是src有时候对于资产的导出，有些.g*v，对于脚本小子肯定是要绕开的，手动摘除非常慢，效率不高，别问，问就是我... ;所以就萌生了这个，总的说，逻辑不难，有很多注释还都是中文的，懂的都懂，想要进一步做优化或者完善补充的随意发挥，源码就仍这了

# 使用

我这里环境是Python 3.10.7

直接运行文件下的rule.py；

- **python rule.py -h#使用帮助**

  ![](https://github.com/ZXGbilibili/Rule-GL/blob/main/img/41126213104.png)

- **python rule.py -ul #规则管理模块**

  ![image](https://github.com/ZXGbilibili/Rule-GL/blob/main/img/202434534543.png)

- **python .\rule.py -u #指定文件路径 默认输出到当前位置，文件名+时间戳**

  ![](https://github.com/ZXGbilibili/Rule-GL/blob/main/img/1126213856.png)

- **python .\rule.py -u  url.txt  -o  output.txt  指定输出**

  ![](https://github.com/ZXGbilibili/Rule-GL/blob/main/img/241126213006.png)
  
  ![](https://github.com/ZXGbilibili/Rule-GL/blob/main/img/41126213013.png)

# 关于后期

取决于需求吧，遇到了合适的在加

