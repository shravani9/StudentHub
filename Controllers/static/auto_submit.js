window.onload = function() {
// Onload event of Javascript
// Initializing timer variable
var x = 20;
var y = document.getElementById("timer");
// Display count down for 20s
setInterval(function(){
if (x <= 21 && x >= 1){
x--;
y.innerHTML = '' + x + '';
if (x == 1){
x = 21;
}
}
}, 1000);
// Form Submitting after 20s
var auto_refresh = setInterval(function(){
submitform();
}, 20000);
// Form submit function
function submitform(){
alert('Form is submitting.....');
document.getElementById("myForm").submit();
}
