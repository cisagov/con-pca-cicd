"""Generates an SVG Chart"""
import math
import numpy as np 
      
class ChartGenerator():
    
    def createList(self, r1, r2, step): 
        return np.arange(r1, r2+1, step) 

    def determineTicks(self, range):
        #determines the appropriate scale 
        #default number of lines/ticks is 8         
        tickCount = 8
        unroundedTickSize = range/(tickCount-1)
        x = math.ceil(math.log10(unroundedTickSize)-1)
        pow10x = math.pow(10, x)
        roundedTickRange = math.ceil(unroundedTickSize / pow10x) * pow10x
        return roundedTickRange


    def generateSvg(self, legendStrings, values):
        maxv = max(values)
        minv = min(values)
        range = max-min
        tickRange = self.determineTicks(range)
        # from min to max
        # step tick range and write lines
        # then write bars
        # return string

        #

        topRange = round(maxv+tickRange,)
        #self.createList(0,  )

        svg_strg = """"<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" class="chart" width="450" height="300" aria-labelledby="title desc" role="img">
            <title id="title">STATISTICS BY LEVEL</title>
            <!--this needs to be dynamic--><desc id="units-achieved">0; 50; 100; 150; 200; 250; 300; 350; 400;</desc>
            <g class="measure-line">
            <line x1="30" y1="5" x2="500" y2="5" style="stroke:#BAD6E4;stroke-width:2"/>
            <line x1="30" y1="35" x2="500" y2="35" style="stroke:#BAD6E4;stroke-width:2"/>
            <line x1="30" y1="65" x2="500" y2="65" style="stroke:#BAD6E4;stroke-width:2"/>
            <line x1="30" y1="95" x2="500" y2="95" style="stroke:#BAD6E4;stroke-width:2"/>
            <line x1="30" y1="125" x2="500" y2="125" style="stroke:#BAD6E4;stroke-width:2"/>
            <line x1="30" y1="155" x2="500" y2="155" style="stroke:#BAD6E4;stroke-width:2"/>
            <line x1="30" y1="185" x2="500" y2="185" style="stroke:#BAD6E4;stroke-width:2"/>
            <line x1="30" y1="215" x2="500" y2="215" style="stroke:#BAD6E4;stroke-width:2"/>
            <line x1="30" y1="245" x2="500" y2="245" style="stroke:#BAD6E4;stroke-width:2"/>
            
            <!--this needs to be dynamic-->
            <text x="15" y="245" class="caption" dy=".35em">0</text>
            <text x="8" y="215" class="caption" dy=".35em">50</text>
            <text x="0" y="185" class="caption" dy=".35em">100</text>
            <text x="0" y="155" class="caption" dy=".35em">150</text>
            <text x="0" y="125" class="caption" dy=".35em">200</text>
            <text x="0" y="95" class="caption" dy=".35em">250</text>
            <text x="0" y="65" class="caption" dy=".35em">300</text>
            <text x="0" y="35" class="caption" dy=".35em">350</text>
            <text x="0" y="5" class="caption" dy=".35em">400</text>
            </g>
             <!--this needs to be dynamic-->
            <desc id="email-action">Sent; Opened; Clicked; Submitted; Reported</desc>
            <g>
            <rect style="fill:#164A91;" width="15" height="200" x="60" y="45"></rect>
            <rect style="fill:#FDC010;" width="15" height="200" x="80" y="45"></rect>
            <rect style="fill:#1979a7" width="15" height="200" x="100" y="45"></rect>
            <text x="70" y="260" class="caption" dy=".35em">Sent</text>
            </g>
            <g>
            <rect style="fill:#164A91;" width="15" height="180" x="150" y="65"></rect>
            <rect style="fill:#FDC010;" width="15" height="180" x="170" y="65"></rect>
            <rect style="fill:#1979a7" width="15" height="180" x="190" y="65"></rect>
            <text x="150" y="260" class="caption" dy=".35em">Opened</text>
            </g>
            <g>
            <rect style="fill:#164A91;" width="15" height="200" x="240" y="45"></rect>
            <rect style="fill:#FDC010;" width="15" height="200" x="260" y="45"></rect>
            <rect style="fill:#1979a7" width="15" height="200" x="280" y="45"></rect>
            <text x="240" y="260" class="caption" dy=".35em">Clicked</text>
            </g>
            <g>
            <rect style="fill:#164A91;" width="15" height="200" x="330" y="45"></rect>
            <rect style="fill:#FDC010;" width="15" height="200" x="350" y="45"></rect>
            <rect style="fill:#1979a7" width="15" height="200" x="370" y="45"></rect>
            <text x="322" y="260" class="caption" dy=".35em">Submitted</text>
            </g>
            <g>
            <rect style="fill:#164A91;" width="15" height="200" x="420" y="45"></rect>
            <rect style="fill:#FDC010;" width="15" height="200" x="440" y="45"></rect>
            <rect style="fill:#1979a7" width="15" height="200" x="460" y="45"></rect>
            <text x="415" y="260" class="caption" dy=".35em">Reported</text>
            </g>
            </svg>"""
        return svg_strg


# Driver Code 
r1, r2 = 0, 450


chartGen = ChartGenerator()
print(chartGen.createList(r1, r2, 50)) 

headers = ["Sent","Opened","Clicked","Submitted","Reported"]
values = [85,85,85,65,65,65,35,35,35,25,25,25,15,15,15]
print(chartGen.generateSvg(headers,values))
    