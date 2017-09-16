var a = document.querySelectorAll(".col-product-name  a")
for (var info of a) { console.log(info.href.split("=")[1]); }
