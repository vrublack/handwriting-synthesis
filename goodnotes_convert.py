import re
#from matplotlib import pyplot as plt

def write_IAM_format(strokes, output_fname):
    header = '<?xml version="1.0" encoding="ISO-8859-1"?><StrokeSet>'
    footer = '</StrokeSet>'

    with open(output_fname, 'w') as f:
        f.write(header)
        for s in strokes:
            f.write('<Stroke>')
            for i in range(len(s[0])):
                f.write('<Point x="%f" y="%f"/>' % (s[0][i], s[1][i]))
            f.write('</Stroke>')
        f.write(footer)
        f.flush()

def extract_d_from_svg(svg):
    strokes = []
    for m in re.finditer(r'(?<![\w])d="(.*?)"', svg):
        match_str = m.group(0)
        stroke_x, stroke_y = path_to_points(match_str)
        strokes.append((stroke_x, stroke_y))

    x_min = None
    y_min = None
    for s in strokes:
        x_m = min(s[0])
        if x_min is None or x_m < x_min:
            x_min = x_m
        y_m = min(s[1])
        if y_min is None or y_m < y_min:
            y_min = y_m

    for s in strokes:
        for i in range(len(s[0])):
            s[0][i] -= x_min
            s[1][i] -= y_min

    # plt.scatter(all_x, all_y)
    # max_val = max(max(all_x), max(all_y))
    # plt.xlim(0, max_val)
    # plt.ylim(0, max_val)
    # plt.show()

    return strokes

def path_to_points(svg_d):
    last_x = 0
    last_y = 0
    all_x = []
    all_y = []
    for m in re.finditer(r'm.*?(?=c)', svg_d):
        match_str = m.group(0)
        delta_x = float(match_str[2:].split(',')[0])
        delta_y = float(match_str[2:].split(',')[1])
        last_x += delta_x
        last_y += delta_y
        all_x.append(last_x)
        all_y.append(-last_y)
        print('%f, %f' % (last_x, last_y))

    return all_x, all_y



if __name__ == '__main__':
    with open("C:\Users\Valentin\Handwriting Synthesis\sentence2.svg") as f:
        strokes = extract_d_from_svg('\n'.join(f.readlines()))
        write_IAM_format(strokes, 'sentence2-iam.xml')