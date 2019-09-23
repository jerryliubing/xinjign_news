function getCookie(name) {
    var r = document.cookie.match("\\b" + name + "=([^;]*)\\b");
    return r ? r[1] : undefined;
}


$(function () {
    // 禁止浏览器对于表单的默认行为
    e.preventDefault();
    // $(this)表示表单对象
    // ajaxSubmit()方法由jquery.form.min.js提供,用于ajax的方式上传文件
    $(this).ajaxSubmit({
        url: "/user/pic",   // 请求路径
        type: "post",   // 请求方式
        dataType: "json",   // 数据类型
        success: function (data) {
            // 更新当前页面头像
            $(".now_user_pic").attr("src", data.avatar);
            // 更新左侧头像
            $(".user_center_pic img", window.parent.document).attr("src", data.avatar);
            // 更新右上角头像
            $(".lgin_pic", window.parent.document).attr("src", data.avatar);
        }
    })
});