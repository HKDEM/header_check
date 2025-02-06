from flask import Flask, request, os
import uuid
app = Flask(__name__)
UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'jpg', 'png'}  # İzin verilen dosya uzantıları
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS
@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        if 'file' not in request.files:
            return 'Dosya seçilmedi'
        file = request.files['file']
        if file.filename == '':
            return 'Dosya seçilmedi'
        if file and allowed_file(file.filename):
            # Güvenli olmayan kısım: Dosya adını doğrudan kullanarak bir yol oluşturuyoruz
            # Bu, dizin geçişi (path traversal) saldırılarına yol açabilir
            # filename = file.filename  # GÜVENLİ DEĞİL!
            # Güvenli kısım: Rastgele bir dosya adı oluşturuyoruz
            filename = str(uuid.uuid4()) + '.' + file.filename.rsplit('.', 1)[1]
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            return 'Dosya yüklendi'
        else:
            return 'İzin verilmeyen dosya uzantısı'
    return '''
    <!doctype html>
    <html>
    <head>
        <title>Dosya Yükleme</title>
    </head>
    <body>
        <h1>Dosya Yükleme</h1>
        <form method="POST" enctype="multipart/form-data">
            <input type="file" name="file">
            <input type="submit" value="Yükle">
        </form>
    </body>
    </html>
    '''
if __name__ == '__main__':
    app.run(debug=True)




NEW







