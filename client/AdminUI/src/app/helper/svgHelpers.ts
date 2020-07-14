
/**
 * Given the numerator and total calculate and
 * return the svg circle.
 */
export function drawSvgCircle(numerator: number, denominator: number) {
    const ratio: number = (numerator ?? 0) / (denominator ?? 1);
    const percentage: number = ratio * 100;
    const remainingPercentage: number = 100 - percentage;
    const svgString = '<svg width="100%" height="100%" viewBox="0 0 42 42" class="donut" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">'
        + '<circle class="donut-hole" cx="21" cy="21" r="14" fill="#fff"></circle>'
        + '<circle class="donut-ring" cx="21" cy="21" r="14" fill="transparent" stroke="#cecece" stroke-width="6"></circle>'
        + '<circle class="donut-segment" cx="21" cy="21" r="14" fill="transparent" stroke="#164A91" stroke-width="6" '
        + `stroke-dasharray="${percentage} ${remainingPercentage}" stroke-dashoffset="25"></circle>`
        + '</svg>';
    return svgString;
}

/**
 * Returns an SVG representation of a complex bar chart.
 * The input is an array of numbers representing raw counts of
 * sent low, medium high, opened low, medium, high, clicked low, med, high, submitted, reported
 */
export function drawSvgStatisticByLevel(values: number[]) {
//     const maxv: number = Math.max(values);
//     const tick_range = self.get_ticks(maxv);
//     // from min to max
//     // step tick range and write lines
//     // then write bars
//     // return string

//     let topRange = self.myround(maxv, tick_range);
//     if (topRange > maxv) {

//     }
//     topRange = topRange if topRange > maxv else topRange + tick_range
//     y_axis = self.get_ylist(0, topRange, tick_range)[:: -1]

//     y_axis_str = " ".join([f"{i};" for i in y_axis])

//     const svg_strg_header_1 = '<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" class="chart" width="450" height="300" aria-labelledby="title desc" role="img">'
//         + '<title id="title" > STATISTICS BY LEVEL < /title>'
//         + '< !--this needs to be dynamic-- > <desc id="units-achieved" > { y_axis_str } < /desc>'
//         + '< g class="measure-line" >';

//     const y_start = 5;
//     const dist_between_bars = self.chart_height / len(y_axis)
//     const svg_strg_axis_2 = "".join(
//         map(
//             str,
//             [
//                 f"""<line x1="30" y1="{ int((index + 1) * dist_between_bars)} " x2="500" y2="{ int((index + 1) * dist_between_bars) } " style="stroke:#BAD6E4; stroke - width: 2"/>"""
// for index in range(0, len(y_axis))
//                 ],
//             )
//         )

//     const svg_strg_axis_3 = "".join(
//     map(
//         str,
//         [
//             f"""<text x="8" y="{ int((i + 1) * dist_between_bars)}" class="caption" dy=".35em">{x}</text>"""
//                     for i, x in enumerate(y_axis)
//                 ],
//             )
//         )

// const svg_string_4 = f"""<desc id="email - action">{self.legend}</desc>"""
// const normalized_values = [
//     self.translate_bar(x, topRange, dist_between_bars) for x in values
//         ]
// const yvalues = [self.translate_get_y(x) for x in normalized_values]

// const svg_string_5 = '</g><g>'
//     + '<rect style="fill:#164A91;" width="15" height="{normalized_values[0]}" x="60" y="{yvalues[0]}"></rect>'
//     + '<rect style="fill:#FDC010;" width="15" height="{normalized_values[1]}" x="80" y="{yvalues[1]}"></rect>'
//     + '<rect style="fill:#1979a7" width="15" height="{normalized_values[2]}" x="100" y="{yvalues[2]}"></rect>'
//     + '<text x="70" y="290" class="caption" dy=".35em">Sent</text>'
//     + '</g>'
//     + '<g>'
//     + '<rect style="fill:#164A91;" width="15" height="{normalized_values[3]}" x="150" y="{yvalues[3]}"></rect>'
//     + '<rect style="fill:#FDC010;" width="15" height="{normalized_values[4]}" x="170" y="{yvalues[4]}"></rect>'
//     + '<rect style="fill:#1979a7" width="15" height="{normalized_values[5]}" x="190" y="{yvalues[5]}"></rect>'
//     + '<text x="150" y="290" class="caption" dy=".35em">Opened</text>'
//     + '</g>'
//     + '<g>'
//     + '<rect style="fill:#164A91;" width="15" height="{normalized_values[6]}" x="240" y="{yvalues[6]}"></rect>'
//     + '<rect style="fill:#FDC010;" width="15" height="{normalized_values[7]}" x="260" y="{yvalues[7]}"></rect>'
//     + '<rect style="fill:#1979a7" width="15" height="{normalized_values[8]}" x="280" y="{yvalues[8]}"></rect>'
//     + '<text x="240" y="290" class="caption" dy=".35em">Clicked</text>'
//     + '</g>'
//     + '<g>'
//     + '<rect style="fill:#164A91;" width="15" height="{normalized_values[9]}" x="330" y="{yvalues[9]}"></rect>'
//     + '<rect style="fill:#FDC010;" width="15" height="{normalized_values[10]}" x="350" y="{yvalues[10]}"></rect>'
//     + '<rect style="fill:#1979a7" width="15" height="{normalized_values[11]}" x="370" y="{yvalues[11]}"></rect>'
//     + '<text x="322" y="290" class="caption" dy=".35em">Submitted</text>'
//     + '</g>'
//     + '<g>'
//     + '<rect style="fill:#164A91;" width="15" height="{normalized_values[12]}" x="420" y="{yvalues[12]}"></rect>'
//     + '<rect style="fill:#FDC010;" width="15" height="{normalized_values[13]}" x="440" y="{yvalues[13]}"></rect>'
//     + '<rect style="fill:#1979a7" width="15" height="{normalized_values[14]}" x="460" y="{yvalues[14]}"></rect>'
//     + '<text x="415" y="290" class="caption" dy=".35em">Reported</text>'
//     + '</g>'
//     + '</svg>';
// return (
//     svg_strg_header_1
//     + svg_strg_axis_2
//     + svg_strg_axis_3
//     + svg_string_4
//     + svg_string_5
// );
}
