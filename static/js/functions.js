//全選択・非選択チェックボックスのchangeイベント
/*$(document).on('change', 'thead :checkbox', function() {
     
    update_text();
  
});*/
//各行チェックボックスのchangeイベント
$(document).on('change', 'tbody :checkbox', function() {

    update_text();

}); 


function update_text() {
    let output = '';
    let table = $('#prefecture_table').DataTable();
    //選択項目を取得
    let selected_data = table.column(0).checkboxes.selected();
    for (let i = 0; i < selected_data.length; i++) {
        output += selected_data[i] + ',';
    }
    $('#selection').text(output);
}

function send_text(){

    let output = '';
    let table = $('#prefecture_table').DataTable();
    //選択項目を取得
    let selected_data = table.column(0).checkboxes.selected();

    var text1 = selected_data[0]
    var text2 = selected_data[1]


    //FormData初期化
    var fData = new FormData();

    fData.append('text1', text1);
    fData.append('text2', text2);

    //ajax送信
    $.ajax({
        //配信元のhttpsサーバーに返す場合
        url: '/register',                            
        //別サーバー（今回でいう画像処理サーバー）に返す場合
        //url: 'https://192.168.0.100:12345/register',   
        type: 'POST',
        data: fData ,
        contentType: false,
        processData: false,
        success: function(data, dataType) {
            //非同期で通信成功時に読み出される [200 OK 時]
            console.log('Success', data);
        },
        error: function(XMLHttpRequest, textStatus, errorThrown) {
            //非同期で通信失敗時に読み出される
            console.log('Error : ' + errorThrown);
        }
    });
}

function test_ajax(){
    data = {"hoge": "fuga"};
    json = JSON.stringify(data);  // object型からJSON文字列(string型)に変換
    $.ajax({
        type: "POST",
        url: "/test",
        data: json,
        contentType: "application/json",
        success: function(msg) {
            console.log(msg);
        },
        error: function(msg) {
            console.log("error");
        }
    });
}






  




