(function ($) {
    function getReply(text){
        $.post('/chat', {'msg': text},function(data){
            console.log(data);
            if(data){
                rp_time = new Date();
                rp_str = `<div class="chat-log__item">
                <h3 class="chat-log__author">System <small>`+ rp_time + `</small></h3>
                <div class="chat-log__message">` + data + `</div>
            </div>`;
            $('.chat-log').append(rp_str);
            }
        })
    }

    $('#chat_form').submit(function(e){
        debugger;
        e.preventDefault();
        let txt = $('#txt_input').val().trim();
        if (!txt)
            return;
        time = new Date();
        str = `<div class="chat-log__item chat-log__item--own">
        <h3 class="chat-log__author">You <small>`+ time +`</small></h3>
        <div class="chat-log__message">` + txt + `</div>
        </div>`;
        $('.chat-log').append(str);
        getReply(txt);
    });



})(jQuery);