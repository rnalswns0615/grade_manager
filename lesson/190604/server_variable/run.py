from flask import Flask, render_template
app = Flask(__name__)


@app.route("/run")
def template_test():
	my_string = "나는 스파이더맨이야."
	my_list = [0,1,2,3,4,5]
	return render_template('template.html', my_string=my_string, my_list=my_list)

if __name__ == '__main__':
	app.run(debug=True, port=8080)
