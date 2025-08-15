
window.onload = initClock;
	
$(document).ready( function() {
    var now = new Date();
    now.setMinutes(now.getMinutes() - now.getTimezoneOffset());
    document.getElementById('fecha_inicio').value = now.toISOString().slice(0,16);
    document.getElementById('fecha_fin').value = now.toISOString().slice(0,16);
    
    actualiza_actividades();

    jQuery('#cod_subp').empty();
    ajax('subproyecto', ['cod_proy'], 'cod_subp');
    jQuery('#cod_bd').empty();
    ajax('func_bd', ['cod_servidor'], 'cod_bd');
    
    document.getElementById("incid_otros").checked = false;

});


function fade(){
    $('#fade').toggle();
}

function fade2(){
    $('#fade2').toggle();
}

function fade3(){
    $('#fade3').toggle();
}

$('form').submit(function(){
			// Validando los campos obligatorios
			flag = true;
			var 
			campos=$('.obligatorio');
			campos.each(function(){
				if(!$(this).val()){
					//alert('validando campos obligatorio');
					 flag = false;
				}});

			  var inicio = new Date(document.getElementById("fecha_inicio").value);
        var fin = new Date(document.getElementById("fecha_fin").value);
        var fechaActual = new Date();
        if (fin < inicio){
              alert("La fecha final de la actividad debe ser mayor a la fecha inicial");
              return false;
        }
    

        else  if(!flag){
                alert('Faltó llenar algún campo ó algún valor está en cero');
                return false;
        }}
);
	

$('#cod_proyx').change(function(){	
			alert($(cod_proy).val());
});


$('#fecha_iniciox').change(function(){  
      fecha = new Date(document.getElementById("fecha_inicio").value);
      document.getElementById("fecha_fin").value = fecha;
});


function actualiza_actividades(){
		ajax('{{=URL("default", "func_mac_sd")}}',['fecha_inicio'], 'act');	
			jQuery('#act').show();
}


function valida_fechas() {
        var inicio = new Date(document.getElementById("fecha_inicio").value);
        var fin = new Date(document.getElementById("fecha_fin").value);
        var actualDate = new Date();
        if (fin < inicio){
              alert("La fecha final de la actividad debe ser mayor a la fecha inicial");
        }
        if (fin > actualDate){
           alert("La fecha fin mayor a la fecha actual"); 
        }

        if (inicio > actualDate){
           alert("La fecha inicio mayor a la fecha actual"); 
        }
    }

function resta(){

  var now = new Date();
  var dia_actual = now.getDate();
  var inicio = new Date(document.getElementById("fecha_inicio").value);
  var fin = new Date(document.getElementById("fecha_fin").value);

  //if (dia_actual == inicio.getDate()){
  
      var hi = inicio.getTime();
      var hf = fin.getTime();
      var extras = 0;

      var first = inicio.getDate() - inicio.getDay(); //domingo del fin de semana
      var last =  first + 6; //sabado del fin de semana

      var dia_semana = inicio.getDay(); // dia de la semana (0..6) 6-sabado, 0-domingo

      if (dia_semana == 0 || dia_semana == 6 ){
        //alert('Fin de semana');
        if (hi <= hf)
      {
          var difference = Math.abs(fin-inicio);
          var horas = difference / 1000 / 60 / 60;
            document.getElementById("horas_laboradas").value = '0.00';   
            document.getElementById("horas_extras").value = horas.toFixed(2); 
            //document.getElementById("horas_extras").value = dia_semana; 
      
      } else { 
            document.getElementById("horas_laboradas").value = '0.00';   
            document.getElementById("horas_extras").value = '0.00'; 
      }
        
      } 
      else 
      {
      if (hi <= hf)
      {
          var difference = Math.abs(fin-inicio);
          var horas = difference / 1000 / 60 / 60;
          //horas = convierte_60(horas);
          //horas = horas / 60 ;
          extras = extra(); 
          if (extras > 0)
          {
             horas = horas - extras;
            document.getElementById("horas_laboradas").value = horas.toFixed(2); 
          } else {
            document.getElementById("horas_laboradas").value = horas.toFixed(2); 
            //document.getElementById("horas_extras").value = dia_semana; 
          }
      } else { 
            document.getElementById("horas_laboradas").value = '0.00';   
            document.getElementById("horas_extras").value = '0.00'; 
      }
    }
}


function convierte_60(h){
  h = (h * 60) ;
  return h;
}

function pad(n) {
    return n<10 ? '0'+n : n
}



function extra(){
  inicio = new Date(document.getElementById("fecha_inicio").value);
  fin = new Date(document.getElementById("fecha_fin").value);
 
  var i_hora8am = new Date(inicio.getFullYear(), inicio.getMonth(), inicio.getDate(), 8, 0, 0  );
  var i_hora5pm = new Date(inicio.getFullYear(), inicio.getMonth(), inicio.getDate(), 17, 0, 0  );
  var i_hora23 = new Date(inicio.getFullYear(), inicio.getMonth(), inicio.getDate(), 23, 59, 59  );

  var f_hora8am = new Date(fin.getFullYear(), fin.getMonth(), fin.getDate(), 8, 0, 0  );
  var f_hora5pm = new Date(fin.getFullYear(), fin.getMonth(), fin.getDate(), 17, 0, 0  );
  var f_hora23 = new Date(fin.getFullYear(), fin.getMonth(), fin.getDate(), 23, 59, 59  );
  var f_hora00 = new Date(fin.getFullYear(), fin.getMonth(), fin.getDate(), 0, 0, 1  );
  var f_hora7am = new Date(fin.getFullYear(), fin.getMonth(), fin.getDate(), 7, 59, 59  );
  var diferencia_dias = Math.trunc((fin.getTime() - inicio.getTime())/(1000 * 60 * 60 * 24));


  if (inicio.getDate() == fin.getDate()){
    if (inicio < i_hora8am && (fin >= f_hora8am && fin < f_hora5pm) ){
      a = calcula_diferencia(i_hora8am, inicio);
      horas = a;
    }
    else if (inicio < i_hora8am && fin >= f_hora5pm){
      a = calcula_diferencia(i_hora8am, inicio);
      b  = calcula_diferencia(fin,f_hora5pm);
      horas = a + b;
    }
    else if (fin >= f_hora5pm && (inicio >= i_hora8am && inicio < i_hora5pm)){
      a = calcula_diferencia(f_hora5pm, fin);
      horas = a;
    }
    else if (inicio < i_hora8am && fin < f_hora8am || inicio >= i_hora5pm && fin >= f_hora5pm){
        a = calcula_diferencia(fin, inicio);
        horas = a;  
    }
    else{
      horas=0;
    }

  }
 

  else if ( (fin.getDate() - inicio.getDate()) == 1 ){
     //alert( fin.getDate() - inicio.getDate() )
    if (inicio <= i_hora8am && fin <= f_hora7am){
        a = calcula_diferencia(i_hora8am, inicio);
        b = 7;
        c = calcula_diferencia(fin, f_hora00);  
        horas = a + b + c ;
    }
    if (inicio <= i_hora8am && ( fin >= f_hora7am && fin <= f_hora5pm) ){
        a = calcula_diferencia(i_hora8am, inicio);
        b = 7;
        c = 8;
        horas = a + b + c ;
    }
    else if ( (inicio >= i_hora8am && inicio <= i_hora5pm) && fin <= f_hora7am){
    
        a = 7;
        b = calcula_diferencia(fin, f_hora00);  
        horas = a + b;
    }
    else if ( (inicio >= i_hora8am && inicio <= i_hora5pm) && (fin >= f_hora7am && fin <= f_hora5pm) ){
        a = 7;
        b = 8;  
        horas = a + b;
    }
    else if ( (inicio >= i_hora8am && inicio <= i_hora5pm) && (fin >= f_hora5pm) ){
        //alert('paso1')
        a = 7;
        b = 8;
        d = calcula_diferencia(fin, f_hora5pm);  
        horas = a + b + d;
    }
    
   else if (inicio <= i_hora8am && fin >= f_hora5pm ){
        a = calcula_diferencia(i_hora8am, inicio);
        b = 7;
        c = 8;
        d = calcula_diferencia(fin, f_hora5pm);
        horas = a + b + c + d;
    }
   else if ( inicio >= i_hora5pm && fin <= f_hora7am){
        a = calcula_diferencia(i_hora23, inicio);
        b = calcula_diferencia(fin, f_hora00);  
        horas = a + b;
    }
    else if (inicio >= i_hora5pm && (fin >= f_hora8am && fin <= f_hora5pm) ){
        a = calcula_diferencia(i_hora23, inicio);
        b = 8;  
        horas = a + b;  
    }
    else if (inicio >= i_hora5pm && ( fin >= f_hora5pm) ){
        a = calcula_diferencia(i_hora23, inicio);
        b = 13;
        c = calcula_diferencia(fin, f_hora5pm);
        horas = a + b + c;
    }
    else if (fin >= f_hora5pm){
        a = calcula_diferencia(fin, f_hora5pm)
        b = calcula_diferencia(i_hora8am, inicio);
        c = calcula_diferencia(f_hora5pm, fin);
        horas = a + b + c;
    }
}

else if ( (fin.getDate() - inicio.getDate()) > 1) {
   //alert( fin.getDate() - inicio.getDate() )
 
    if (inicio <= i_hora8am && fin <= f_hora7am){
        a = calcula_diferencia(i_hora8am, inicio);
        b = 7 * diferencia_dias;
        c = calcula_diferencia(fin, f_hora00);  
        horas = a + b + c ;
    }
    if (inicio <= i_hora8am && ( fin >= f_hora7am && fin <= f_hora5pm) ){
        a = calcula_diferencia(i_hora8am, inicio);
        b = 7 * diferencia_dias;
        c = 8 * diferencia_dias;
        horas = a + b + c ;
    }
    else if ( (inicio >= i_hora8am && inicio <= i_hora5pm) && fin <= f_hora7am){
        a = 7 * diferencia_dias;
        b = calcula_diferencia(fin, f_hora00);  
        horas = a + b;
    }
    else if ( (inicio >= i_hora8am && inicio <= i_hora5pm) && (fin >= f_hora7am && fin <= f_hora5pm) ){
        a = 7 * diferencia_dias;
        b = 8 * diferencia_dias;  
        horas = a + b;
    }
     else if ( (inicio >= i_hora8am && inicio <= i_hora5pm) && (fin >= f_hora5pm) ){
        a = 7 * diferencia_dias;
        b = 8 * diferencia_dias;
        d = calcula_diferencia(fin, f_hora5pm);  
        horas = a + b + d;
    }
    else if (inicio <= i_hora8am && fin >= f_hora5pm ){
        a = calcula_diferencia(i_hora8am, inicio);
        b = 7 * diferencia_dias;
        c = 8 * diferencia_dias;
        d = calcula_diferencia(fin, f_hora5pm);
        horas = a + b + c + d;
    }
    else if ( inicio >= i_hora5pm && fin <= f_hora7am){
        a = calcula_diferencia(i_hora23, inicio);
        b = calcula_diferencia(fin, f_hora00); 
        c = 15 * diferencia_dias; 
        horas = a + b + c ;
    }
    else if (inicio >= i_hora5pm && (fin >= f_hora8am && fin <= f_hora5pm) ){
        a = calcula_diferencia(i_hora23, inicio);
        b = 8 * diferencia_dias;  
        horas = a + b;  
    }
    else if (inicio >= i_hora5pm && ( fin >= f_hora5pm) ){
        a = calcula_diferencia(i_hora23, inicio);
        b = 13 * diferencia_dias;
        c = calcula_diferencia(fin, f_hora5pm);
        horas = a + b + c;
    }
    else if (fin >= f_hora5pm){
        //alert('paso')
        a = calcula_diferencia(fin, f_hora5pm)
        b = calcula_diferencia(i_hora8am, inicio);
        c = calcula_diferencia(f_hora5pm, fin);
        horas = a + b + c;
    }
}

  //horas = convierte_60(horas);
  document.getElementById("horas_extras").value = (horas).toFixed(2) ;
  return horas;
}



function calcula_diferencia(h1, h2){
    return (Math.abs(h1-h2) /1000 / 60 / 60);
}

function restaTiempoFecha(objDateInicio, objDateFin){
    var diferencia = Math.abs(objDateFin.getTime() - objDateInicio.getTime());
    var horas = diferencia / (60 * 60000);
    alert(horas);
    return horas;
  }

function getDateAgo(date, days) {
  let dateCopy = new Date(date);
  dateCopy.setDate(date.getDate() - days);
  return dateCopy.getDate();
}

function getLastDayOfMonth(year, month) {
  let date = new Date(year, month + 1, 0);
  return date.getDate();
}

function getSecondsToday() {
  let d = new Date();
  return d.getHours() * 3600 + d.getMinutes() * 60 + d.getSeconds();
}

function getSecondsToTomorrow() {
  let now = new Date();
  let hour = now.getHours();
  let minutes = now.getMinutes();
  let seconds = now.getSeconds();
  let totalSecondsToday = (hour * 60 + minutes) * 60 + seconds;
  let totalSecondsInADay = 86400;
  return totalSecondsInADay - totalSecondsToday;
}

function initClock(){
  var now = new Date();
  var hr = now.getHours();
  var min = now.getMinutes();
  var sec = now.getSeconds();
  if (min < 10) min = "0" + min;
  if (sec < 10) sec = "0" + sec;
  //document.getElementById('picture').innerHTML = "{{URL('download', args=pic)}}"  ;
  document.getElementById('clockDisplay').innerHTML = " Registro de actividades - hora : " + hr + ":" + min + ":" + sec ;
  setTimeout('initClock()', 500);

}