"""Generates an SVG Chart"""
import math
import numpy as np

class ChartGenerator():
    chart_height = 275    
    def translateBar(self, barHeight, maxvalue, first_offSet):
        #moves bar to align it at the bottom axis
        #determine chart height
        #subtract bar height from 100 to get starting point
        factor = (self.chart_height-first_offSet)/maxvalue
        return int(factor*barHeight)
     
    def translateGetY(self, barHeight):
        #moves bar to align it at the bottom axis
        #determine chart height
        #subtract bar height from 100 to get starting point    
        return int(self.chart_height - barHeight)

    def createList(self, r1, r2, step): 
        return np.arange(r1, r2+1, step) 

    def determineTicks(self, range):
        #determines the appropriate scale 
        #default number of lines/ticks is 8         
        if range < 10:
            return 1
        if range < 50:
            return 5
        if range < 100:
            return 10
        if range < 500: 
            return 50
        if range < 1000:
            return 100
        if range < 10000:
            return 1000
        else:
            return 1000
        
        
        return 

    def myround(self, x, base):
        return base * round(x/base)

    def generateSvg(self, legendStrings, values):
        maxv = max(values)        
        tick_range = self.determineTicks(maxv)
        # from min to max
        # step tick range and write lines
        # then write bars
        # return string

        topRange = self.myround(maxv,tick_range)
        topRange = topRange if topRange > maxv else topRange+tick_range        
        y_axis = self.createList(0,topRange,tick_range)
        
        y_axisList = " ".join([f"{i};" for i in y_axis])
        #print(y_axisList)

        svg_strg_header_1 = f"""<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" class="chart" width="450" height="300" aria-labelledby="title desc" role="img">
            <title id="title">STATISTICS BY LEVEL</title>
            <!--this needs to be dynamic--><desc id="units-achieved">{y_axisList}</desc>
            <g class="measure-line">"""
         
        svg_strg_2 =f"""<desc id="email-action">{legendStrings}</desc>"""
        dist_between_bars = self.chart_height / len(y_axis)
        
        svg_strg_axis_1 = "".join(
            map(
                str,
                [
                    f"""<line x1="35" y1="{int((i+1) * dist_between_bars)}" x2="500" y2="{int((i+1) * dist_between_bars)}" style="stroke:#BAD6E4;stroke-width:2"/>\n"""                    
                    for i, x in enumerate(y_axis)
                ],
            )
        )
        svg_strg_axis_2 = "".join(
            map(
                str,
                [                    
                    f"""<text x="" y="{int((i+1) * dist_between_bars)}" class="caption" dy=".35em">{x}</text>\n"""
                    for i, x in enumerate(reversed(y_axis))
                ],
            )
        )
        

        normalized_values = [self.translateBar(x,topRange,dist_between_bars) for x in values] 
        yvalues = [self.translateGetY(x) for x in normalized_values] 
        svg_string_4 = f"""</g><g>
            <rect style="fill:#164A91;" width="15" height="{normalized_values[0]}" x="60" y="{yvalues[0]}"></rect>
         <rect style="fill:#FDC010;" width="15" height="{normalized_values[1]}" x="80" y="{yvalues[1]}"></rect>
            <rect style="fill:#1979a7" width="15" height="{normalized_values[2]}" x="100" y="{yvalues[2]}"></rect>
            <text x="70" y="290" class="caption" dy=".35em">Sent</text>
            </g>
            <g>
            <rect style="fill:#164A91;" width="15" height="{normalized_values[3]}" x="150" y="{yvalues[3]}"></rect>
            <rect style="fill:#FDC010;" width="15" height="{normalized_values[4]}" x="170" y="{yvalues[4]}"></rect>
            <rect style="fill:#1979a7" width="15" height="{normalized_values[5]}" x="190" y="{yvalues[5]}"></rect>
            <text x="150" y="290" class="caption" dy=".35em">Opened</text>
            </g>
            <g>
            <rect style="fill:#164A91;" width="15" height="{normalized_values[6]}" x="240" y="{yvalues[6]}"></rect>
            <rect style="fill:#FDC010;" width="15" height="{normalized_values[7]}" x="260" y="{yvalues[7]}"></rect>
            <rect style="fill:#1979a7" width="15" height="{normalized_values[8]}" x="280" y="{yvalues[8]}"></rect>
            <text x="240" y="290" class="caption" dy=".35em">Clicked</text>
            </g>
            <g>
            <rect style="fill:#164A91;" width="15" height="{normalized_values[9]}" x="330" y="{yvalues[9]}"></rect>
            <rect style="fill:#FDC010;" width="15" height="{normalized_values[10]}" x="350" y="{yvalues[10]}"></rect>
            <rect style="fill:#1979a7" width="15" height="{normalized_values[11]}" x="370" y="{yvalues[11]}"></rect>
            <text x="322" y="290" class="caption" dy=".35em">Submitted</text>
            </g>
            <g>
            <rect style="fill:#164A91;" width="15" height="{normalized_values[12]}" x="420" y="{yvalues[12]}"></rect>
            <rect style="fill:#FDC010;" width="15" height="{normalized_values[13]}" x="440" y="{yvalues[13]}"></rect>
            <rect style="fill:#1979a7" width="15" height="{normalized_values[14]}" x="460" y="{yvalues[14]}"></rect>
            <text x="415" y="290" class="caption" dy=".35em">Reported</text>
            </g>
            </svg>"""
        return svg_strg_header_1 + svg_strg_2 + svg_strg_axis_1 + svg_strg_axis_2  + svg_string_4

