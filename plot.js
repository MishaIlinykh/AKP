var doc = document.getElementById("Canvas");
var field = doc.getContext("2d");
var doc2 = document.getElementById("Canvas2");
var field2 = doc2.getContext("2d");
//var len = plotLine.length;
var colorElement = ['red','black','deeppink','darkmagenta','coral','orange','darkred','darksalmon','indigo','indianred','blue','maroon','navy','olive',
                    'orangered','slategray','teal','thistle','mediumvioletred','dodgerblue','cornflowerblue','green'];
var element = ['T, °C','C','Si','Mn','P','S','Al','Cu','Cr','Mo','Ni','V','Ti','Nb','Ca','Co','W','B','As','Sn','N','Cэ'];
var scrollPos = document.getElementById("parent");

field.font = "14px Times New Roman";
field2.font = "bold 14px Times New Roman";

var checkElem = [];
//var tit = "";
var mouseX = 0;
var mouseY = 0;
var mouseX1 = 0;
var mouseY1 = 0;
var mouseTime = "";
var oldMelting = "";
//-----------------------------------------------------------------------------
function CreateElement()
{
  //----checkbox--------
  var parentDiv = document.getElementById("checkDiv1");
  var parentTab = document.getElementById("el");

  for (var i = 0; i < element.length; i++)
  {
    if (i > element.length/2) {var parentDiv = document.getElementById("checkDiv2");}

    var newElement = document.createElement('label');
    newElement.style = "color:"+colorElement[i];
    parentDiv.appendChild(newElement);
    
    var newCheck = document.createElement('input');
    newCheck.type="checkbox";
    newElement.appendChild(newCheck);
    checkElem[i] = newCheck;

    var newText = document.createElement('label');
    newText.textContent = element[i];
    newElement.appendChild(newText);

    if (i > 0) {
      var newEl = document.createElement('td');
      parentTab.appendChild(newEl);
      newEl.textContent = element[i];
      newEl.width = "50";
    }
  }

  //checkElem[0].checked=true;
  checkElem[1].checked=true;
  checkElem[2].checked=true;
  checkElem[3].checked=true;
  checkElem[21].checked=true;
}
//-----------------------------------------------------------------------------
function plotAxe()
{
  field.beginPath();
  field.strokeStyle="lemonchiffon";
  field.fillStyle = "lemonchiffon";
  field.fillRect(0, 0, field.canvas.width, 420);
  field.fillRect(0, 780, field.canvas.width, field.canvas.height);
  field.stroke();

  //сетка

   hh = parseInt(nowTime[1].substr(1,2),10);
   mm = parseInt(nowTime[1].substr(4,2),10);
   ss = parseInt(nowTime[1].substr(7,2),10);

   tekTime = (hh*3600)+(mm*60)+ss;

   for (var i = 0; i < tekTime; i=i+180) {
      field.beginPath();
      field.lineWidth=1;
      field.strokeStyle="white";
      field.moveTo(i,420);
      field.lineTo(i,780);
      field.stroke();

      YY = parseInt(steelData[2].substr(0,4),10);
      MM = parseInt(steelData[2].substr(5,2),10);
      DD = parseInt(steelData[2].substr(8,2),10);
      hh = parseInt(steelData[2].substr(11,2),10);
      mm = parseInt(steelData[2].substr(14,2),10);
      ss = parseInt(steelData[2].substr(17,2),10);

      ss= ss + i;
      day = Math.floor(ss/86400);
      hour = Math.floor(ss/3600)-(day*86400);
      minutes = Math.floor(ss/60)-(hour*60)-(day*86400);
      seconds = ss-(hour*3600)-(minutes*60)-(day*86400);
      mm = mm + Math.floor(ss/60);
      day = Math.floor(mm/1440);
      hour = Math.floor(mm/60)-(day*1440);
      minutes = mm-(hour*60)-(day*1440);
      hh = hh + Math.floor(mm/60);
      day = Math.floor(hh/24);
      hour = hh-(day*24);
      DD = DD + Math.floor(hh/24);
      day = DD;
      if (MM < 10) {MMS = "0"+MM;} else {MMS = MM;}
      if (day < 10) {dayS = "0"+day;} else {dayS = day;}
      if (hour < 10) {hourS = "0"+hour;} else {hourS = hour;}
      if (minutes < 10) {minutesS = "0"+minutes;} else {minutesS = minutes;}
      if (seconds < 10) {secondsS = "0"+seconds;} else {secondsS = seconds;}
      plTime = YY+"-"+MMS+"-"+dayS+" "+ hourS + ":" + minutesS + ":" + secondsS;

      ss = i;
      hour = Math.floor(ss/3600);//-(day*86400);
      minutes = Math.floor(ss/60)-(hour*60);//-(day*86400);
      seconds = ss-(hour*3600)-(minutes*60);//-(day*86400);
      if (hour < 10) {hourS = "0"+hour;} else {hourS = hour;}
      if (minutes < 10) {minutesS = "0"+minutes;} else {minutesS = minutes;}
      if (seconds < 10) {secondsS = "0"+seconds;} else {secondsS = seconds;}
      relTime = hourS + ":" + minutesS + ":" + secondsS;

      if (i > 0) {
        field.strokeStyle="black";
        field.fillStyle = "black";
        field.fillText(relTime,i-25,800);
        field.fillText(plTime,i-50,820);
      }
   }

  var t = document.getElementById("time");
  t.textContent = " Текущее время: " + nowTime[0];
  t = document.getElementById("timeInt");
  t.textContent = " Продолжительность плавки: " + nowTime[1];
}
//--------------------------------------------------------------------------
function PlotLabel()
{
  field2.lineWidth=2;
  field2.clearRect(0, 0, field2.canvas.width, field2.canvas.height);
  k = 0;
  dx = 0;
  tit = "";
  for (var i = 0; i < localData.length; i++) {
    //if (checkElem[i].checked === true)
    //{
      field2.beginPath();
      field2.fillStyle = "lightgray";
      field2.strokeStyle = colorElement[i];
      x = plotTime[0][plotTime[0].length-1];
      if (startTime > 0) {          
          if (localData[i][4] === 1 && x >= startTime) {field2.fillStyle = "yellow";}
      }
      //if (localData[i][4] === 1 && timePoint.length > 0) {field2.fillStyle = "yellow";}
      field2.rect(5+dx*120, k*50+5, 115, 40);
      field2.closePath();
      field2.fill();
      field2.stroke();
      field2.strokeStyle = "black";
      field2.fillStyle = "black";
      field2.fillText(element[i],10+dx*120,k*50+20);
      if (startTime > 0) {
        if (x >= startTime && i > 0) {field2.fillText(localData[i][1]+localData[i][0],10+dx*120,k*50+38);}
      }
      //if (timePoint.length > 0 && i > 0) {field2.fillText(localData[i][1]+localData[i][0],10+dx*120,k*50+38);}
      if (localData[i][3] >= 0 && i > 0){field2.fillText(localData[i][3]+localData[i][0],70+dx*120,k*50+20);}
      if (localData[i][2] >= 0 && i > 0){field2.fillText(localData[i][2]+localData[i][0],70+dx*120,k*50+38);}

      //if (tempPoint.length > 0 && i === 0) {field2.fillText(localData[i][1]+localData[i][0],10+dx*120,k*50+38);}
      if (tempPoint.length > 0 && i === 0) {field2.fillText(tempPoint[tempPoint.length-1][2],70+dx*120,k*50+20);}
      if (tempPoint.length > 0 && i === 0) {field2.fillText('последний замер',10+dx*120,k*50+38);}
      //if (tempPoint.length > 0 && i === 0){field2.fillText(localData[i][3]+localData[i][0],70+dx*120,k*50+20);}

      k = k + 1;
      if (k >= 10)
      {
        k = 0;
        dx = dx + 1
      }
    //}
  }
  
  if (localData.length <= 0) {
    for (var i = 0; i < localDataC.length; i++) {
      field2.beginPath();
      field2.fillStyle = "lightgray";
      field2.strokeStyle = colorElement[i];
      x = plotTimeC[0][plotTimeC[0].length-1];
      if (startTime > 0) {          
          if (localDataC[i][4] === 1 && x >= startTime) {field2.fillStyle = "yellow";}
      }
      //if (localData[i][4] === 1 && timePoint.length > 0) {field2.fillStyle = "yellow";}
      field2.rect(5+dx*120, k*50+5, 115, 40);
      field2.closePath();
      field2.fill();
      field2.stroke();
      field2.strokeStyle = "black";
      field2.fillStyle = "black";
      field2.fillText(element[i],10+dx*120,k*50+20);
      if (startTime > 0) {
        if (x >= startTime && i > 0) {field2.fillText(localDataC[i][1]+localDataC[i][0],10+dx*120,k*50+38);}
      }
      //if (timePoint.length > 0 && i > 0) {field2.fillText(localData[i][1]+localData[i][0],10+dx*120,k*50+38);}
      if (localDataC[i][3] >= 0 && i > 0){field2.fillText(localDataC[i][3]+localDataC[i][0],70+dx*120,k*50+20);}
      if (localDataC[i][2] >= 0 && i > 0){field2.fillText(localDataC[i][2]+localDataC[i][0],70+dx*120,k*50+38);}

      //if (tempPoint.length > 0 && i === 0) {field2.fillText(localData[i][1]+localData[i][0],10+dx*120,k*50+38);}
      if (tempPoint.length > 0 && i === 0) {field2.fillText(tempPoint[tempPoint.length-1][2],70+dx*120,k*50+20);}
      if (tempPoint.length > 0 && i === 0) {field2.fillText('последний замер',10+dx*120,k*50+38);}
      //if (tempPoint.length > 0 && i === 0){field2.fillText(localData[i][3]+localData[i][0],70+dx*120,k*50+20);}

      k = k + 1;
      if (k >= 10)
      {
        k = 0;
        dx = dx + 1
      }
    }

  }
}
//--------------------------------------------------------------------------
function printNowTime()
{
  if (nowTime.length > 0)
  {
      //время
      var t = document.getElementById("time");
      t.textContent = " Текущее время: " + nowTime[0];
      t = document.getElementById("timeInt");
      t.textContent = " Продолжительность плавки: " + nowTime[1];
  }
  else {
      var t = document.getElementById("time");
      t.textContent = " Текущее время: ";
      t = document.getElementById("timeInt");
      t.textContent = " Продолжительность плавки: ";
  }
}
//--------------------------------------------------------------------------
function plotT()
{
  field.lineWidth=2;
  if (tempPoint.length > 0)
  {
      if (checkElem[0].checked === true)
      {
        field.strokeStyle=colorElement[0];
        field.fillStyle = colorElement[0];
        var xP = tempPoint[0][0];
        var yP = tempPoint[0][1]+300;
    
        field.beginPath();
        field.arc(xP, yP, 3, 0, Math.PI*2, 0);
        field.fill();
        field.stroke();

         for (var i = 1; i < tempPoint.length; i++) {
           field.beginPath();
           xP = tempPoint[i-1][0];
           yP = tempPoint[i-1][1]+300;
           field.moveTo(xP,yP);
           xP = tempPoint[i][0];
           yP = tempPoint[i][1]+300;
           field.lineTo(xP, yP);
           field.stroke();
           field.beginPath();
           field.arc(xP, yP, 3, 0, Math.PI*2, 0);
           field.fill();
           field.stroke();
         }
         field.beginPath();
         xP = tempPoint[tempPoint.length-1][0];
         yP = tempPoint[tempPoint.length-1][1]+300;
         field.moveTo(xP,yP);
         //xP = field.canvas.width;
         if (plotTime.length > 0) {
           xP = plotTime[0][plotTime[0].length - 1];}
         else {
           if (plotTimeC.length > 0) {
             xP = plotTimeC[0][plotTimeC[0].length - 1];}
         }
         field.lineTo(xP, yP);
         field.stroke();
      }
  }
}
//--------------------------------------------------------------------------
function plotP()
{
  field.lineWidth=1;
  var tab = document.getElementById("lab");
  //var tr = document.getElementById("el");
  if (plotPoint.length > 0)
  {
    for (var j = 0; j < plotPoint.length; j++) {

      if (checkElem[j+1].checked === true)
      {
        field.strokeStyle=colorElement[j+1];
        field.fillStyle = colorElement[j+1];

        for (var i = 0; i < plotPoint[j].length; i++) {
          var xP = timePoint[i];
          var yP = plotPoint[j][i]+300;

          field.beginPath();
          field.arc(xP, yP, 3, 0, Math.PI*2, 0);
          field.fill();
          field.stroke();
        }
      }
    }
  }
    if (tab.children.length > 1) {
      m = tab.children.length - 1;
      for (var i = m; i > 0; i--){
        var div = tab.children[i];
        //div.parentNode.removeChild(div);
        tab.removeChild(div);
      }
    }
    //анализы
    //nP.textContent = nP.textContent + ', ' + tab.children.length;
    for (var j = 0; j < timePointR.length; j++) {
      
      var newTr = document.createElement('tr');
      var newEl = document.createElement('td');      
      newTr.appendChild(newEl);
      newEl.textContent = timePointR[j];

      for (var i = 0; i < plotPointR.length; i++) {
        var newEl = document.createElement('td');
        newTr.appendChild(newEl);
        newEl.textContent = plotPointR[i][j];
      // newEl.width = "50";

        if (localData.length > 0) {
          var maxTmp = localData[i+1][3];
          if (maxTmp < 0) {maxTmp = 1000;}
          var minTmp = localData[i+1][2]; }
        else {
          if (localDataC.length > 0) {
            var maxTmp = localDataC[i+1][3];
            if (maxTmp < 0) {maxTmp = 1000;}
            var minTmp = localDataC[i+1][2]; }
        }

        if ((plotPointR[i][j] > minTmp) && (plotPointR[i][j] < maxTmp))
        {
          newEl.style.backgroundColor = "white";
        }
        else
        {
          newEl.style.backgroundColor = "yellow";//"orange";
          newEl.style.color = "purple";
          newEl.style.fontWeight = "bold";
        }
      }
      //tab.insertBefore(newTr, tr);
      tab.appendChild(newTr);
    }
}
//--------------------------------------------------------------------------
function AddAdd(tab,j,mas)
{
        var newTr = document.createElement('tr');

        var newEl = document.createElement('td');      
        newTr.appendChild(newEl);
        newEl.textContent = additive[j][0];

        newEl = document.createElement('td');      
        newTr.appendChild(newEl);
        newEl.textContent = additive[j][1];

        var newEl = document.createElement('td');      
        newTr.appendChild(newEl);
        newEl.textContent = additive[j][2];

        newEl = document.createElement('td');      
        newTr.appendChild(newEl);
        newEl.textContent = additive[j][3];
        newEl.classList.add('tright');
      
        tab.appendChild(newTr);
        mas = mas + additive[j][3];
   return mas;
}
//--------------------------------------------------------------------------
function PrintAdd()
{
    var tab = document.getElementById("additive");
    var m = tab.children.length - 1;
    
    if (m > 0) {
      for (var i = m; i > 0; i--){
        var div = tab.children[i];
        tab.removeChild(div);
      }
    }

    var massa = 0;

//    if (timeSortAd === true)
//    {
//      for (var j = additive.length-1; j >= 0; j--) {
//        massa = AddAdd(tab,j,massa);
//      }
//    }
//    else {
      for (var j = 0; j < additive.length; j++) {
        massa = AddAdd(tab,j,massa);
      }
//    }

    var newTr = document.createElement('tr');    

    var newEl = document.createElement('td');      
    newTr.appendChild(newEl);
    newEl.textContent = "Всего:";
    //newEl.style.backgroundColor = "skyblue";
    newEl.style.borderTopColor = "black";
    newEl.style.borderTopStyle = "solid";
    newEl.style.borderTopWidth = "1pt";
    //newEl.style.fontWeight = "bold";
    newEl.setAttribute("colspan","3",0);

    var newEl = document.createElement('td');      
    newTr.appendChild(newEl);
    newEl.textContent = massa;
    //newEl.style.backgroundColor = "skyblue";
    newEl.style.borderTopColor = "black";
    newEl.style.borderTopStyle = "solid";
    newEl.style.borderTopWidth = "1pt";
    newEl.classList.add('tright');
    //newEl.style.fontWeight = "bold";
      
    tab.appendChild(newTr);
}
//--------------------------------------------------------------------------
function AddRecom(tab,j)
{
        var newTr = document.createElement('tr');

        var newEl = document.createElement('td');      
        newTr.appendChild(newEl);
        newEl.textContent = recom[j][0];

        newEl = document.createElement('td');      
        newTr.appendChild(newEl);
        newEl.textContent = recom[j][1];

        var newEl = document.createElement('td');      
        newTr.appendChild(newEl);
        newEl.textContent = recom[j][2];

        newEl = document.createElement('td');      
        newTr.appendChild(newEl);
        newEl.textContent = recom[j][3];
        newEl.classList.add('tright');
      
        tab.appendChild(newTr);
}
//--------------------------------------------------------------------------
function PrintRecom()
{
    var tab = document.getElementById("recom");
    var m = tab.children.length - 1;
    
    if (m > 0) {
      for (var i = m; i > 0; i--){
        var div = tab.children[i];
        tab.removeChild(div);
      }
    }


      for (var j = 0; j < recom.length; j++) {
        AddRecom(tab,j);
      }

//    var newTr = document.createElement('tr');    
//    var newEl = document.createElement('td');      
//    newTr.appendChild(newEl);
//    tab.appendChild(newTr);
}
//--------------------------------------------------------------------------
function plotGraph()
{
  field.setLineDash([]);
  var nP = document.getElementById("number");

  nP.textContent = "Марка стали: " + steelData[0] + ", номер плавки: " + steelData[1];
  printNowTime();
  var x = 0;
  if (plotLine.length > 0) {
    x = plotTime[0][plotLine[0].length-1]; }
  else {
    if (plotLineC.length > 0) {
      x = plotTimeC[0][plotLineC[0].length-1]; }
  } 
  
  if (x > field.canvas.width)
  {
    field.canvas.width = x;
    scrollPos.scrollLeft = field.canvas.width - 525;
  }
  if (x <= 800)
  {
    field.canvas.width = 800;
    scrollPos.scrollLeft = 0;
  }
  if (oldMelting != steelData[1]) {
    oldMelting = steelData[1];
    scrollPos.scrollTop = 300;
  }
  field.font = "14px Times New Roman";
  field.clearRect(0, 0, field.canvas.width, field.canvas.height);
  PlotLabel();
  plotAxe();
  plotP();
  plotT();
  PrintAdd();
  PrintRecom();
  field.lineWidth=2;

  var ch = plotLine.length;
  if (ch <= 0) {ch = plotLineC.length;}

  for (var j = 1; j < ch; j++) {

    if (checkElem[j].checked === true)
    {
      len = plotLine.length;
      if (len > 0) {
        field.setLineDash([]);
        len = plotLine[j].length;
        field.beginPath();
        field.strokeStyle=colorElement[j];
        var x0 = plotTime[0][0];
        var y0 = plotLine[j][0]+300;
        var i0 = 0;
        //startTime = timePoint[0];
        for (var i = 0; i < len; i ++) {
          x = plotTime[0][i];
          if (startTime > 0) {
            if (x >= startTime && j != 0) {x0 = plotTime[0][i]; y0 = plotLine[j][i]+300; i0 = i; break;}
          //if (x >= tempPoint[0][0] && j === 0) {x0 = plotTime[0][i]; y0 = plotLine[j][i]+300; i0 = i; break;}
          }
        }
        //x = plotTime[0][0];
        var y = plotLine[j][0]+300;
        field.moveTo(x0,y0);

        for (var i = i0; i < len; i ++) {
          x = plotTime[0][i];
          if (startTime > 0) {
            if (x >= startTime)
            {
              y = plotLine[j][i]+300;
              field.lineTo(x, y);
            }
          }
        }
        field.stroke();
      }
      len = plotLineC.length
      if (len > 0) {
        len = plotLineC[j].length
        field.setLineDash([5, 3]);
        field.beginPath();
        field.strokeStyle=colorElement[j];
        var x0 = plotTimeC[0][0];
        var y0 = plotLineC[j][0]+300;
        var i0 = 0;
        //startTime = timePoint[0];
        for (var i = 0; i < len; i ++) {
          x = plotTimeC[0][i];
          if (startTime > 0) {
            if (x >= startTime && j != 0) {x0 = plotTimeC[0][i]; y0 = plotLineC[j][i]+300; i0 = i; break;}
          //if (x >= tempPoint[0][0] && j === 0) {x0 = plotTime[0][i]; y0 = plotLine[j][i]; i0 = i; break;}
          }
        }
        //x = plotTime[0][0];
        var y = plotLineC[j][0]+300;
        field.moveTo(x0,y0);

        for (var i = i0; i < len; i ++) {
          x = plotTimeC[0][i];
          if (startTime > 0) {
            if (x >= startTime)
            {
              y = plotLineC[j][i]+300;
              field.lineTo(x, y);
            }
          }

        }
        field.stroke();
      }
    }
  }
  plotTip(mouseX1,mouseY1);
}
//-----------------------------------------------------------------------------
function getMousePos(canv, evt) {
   var rect = canv.getBoundingClientRect();
   return {
     x: evt.clientX - rect.left,
     y: evt.clientY - rect.top
   };
}
//----------------------------------------------------------------------------
doc.addEventListener('dblclick', function(evt) {
   scrollPos.scrollTop = 300;
   scrollPos.scrollLeft = field.canvas.width - 525;
 }, false);
//----------------------------------------------------------------------------
function plotTip(x,y) {
  flag = false;
  var xP = 0;
  var yP = 0;
  var tmp = "";
  var tmp2 = mouseTime;
  //температура точки
  if ((checkElem[0].checked === true) && (flag === false)) {
    for (var i = 0; i < tempPoint.length; i++) {
       xP = tempPoint[i][0];
       yP = tempPoint[i][1]+300;
       if ((xP>=x-3) && (xP<=x+3) && (yP>=y-3) && (yP<=y+3)) {
          tmp = "T = "+tempPoint[i][2]+"°C";
          tmp2 = tempPoint[i][3];
          flag = true;
          break;
       }
    }
  }
  //химия
  if ((plotPoint.length > 0) && (flag === false))
  {
    for (var j = plotPoint.length-1; j >= 0; j--) {

      if ((checkElem[j+1].checked === true) && (flag === false))
      {
        for (var i = 0; i < plotPoint[j].length; i++) {
          xP = timePoint[i];
          yP = plotPoint[j][i]+300;
          if ((xP>=x-3) && (xP<=x+3) && (yP>=y-3) && (yP<=y+3)) {
            tmp = element[j+1] + ": "+plotPointR[j][i]+localData[j+1][0];
            tmp2 = timePointR[i];
            flag = true;
            break;
          }
        }
      }
    }
  }
  //модель
  if ((plotLine.length > 0) && (flag === false))
  {
    for (var j = plotLine.length-1; j >= 0; j--) {
      if ((checkElem[j].checked === true) && (flag === false))
      {
        if ((plotLine[j].length-1 > 0) && (flag === false)) {
          for (var i = 0; i < plotLine[j].length-1; i++) {
            xt = plotTime[0][i];
            if (startTime > 0) {
              if (xt >= startTime) {
                x0 = plotTime[0][i];
                y0 = plotLine[j][i]+300;
                x2 = plotTime[0][i+1];
                y2 = plotLine[j][i+1]+300;
                xP = x;
                yP = ((xP-x0)*(y2-y0)/(x2-x0))+y0;
                if ((x2>=x) && (x0<=x) && (yP>=y-2) && (yP<=y+2)) {
                  tmp = "Модель "+ element[j] + ": "+ (Math.round(((scale[j][1]-yP+300)/scale[j][0])*10000)/10000) +localData[j][0];
                  //tmp2 = timePointR[i];
                  flag = true;
                  break;
                }
              }
            }
          }
        }
      }
    }
  }

  if (flag) {
    var x1 = x;
    var y1 = y;
    if (x1+138 > scrollPos.scrollLeft+780) {x1 = scrollPos.scrollLeft+780-138;}
    if (y1-43 < scrollPos.scrollTop) {y1 = scrollPos.scrollTop+43;}

    field.setLineDash([]);
    field.strokeStyle = "skyblue";
    field.fillStyle = "lightblue";
    field.lineWidth=1;
    field.beginPath();
    field.rect(x1, y1-44, 138, 43);
    field.closePath();
    field.fill();
    field.stroke();
    field.beginPath();
    field.strokeStyle="black";
    field.fillStyle = "black";
    field.fillText(tmp,x1+5,y1-28);
    field.fillText(tmp2,x1+5,y1-8);
    field.closePath();
    field.stroke();
  }
}
//-----------------------------------------------------------------------------
doc.addEventListener('mousemove', function(evt) {
   var mousePos = getMousePos(doc, evt);
   var message = 'Mouse position: ' + mousePos.x + ', ' + mousePos.y;
   tit = ""
   for (var j = 0; j < plotLine.length; j++) {
     if (checkElem[j].checked === true)
     {
        var op = 10000;
        if (j === 0) {op = 1;}
        tit = tit + element[j] + ": " + Math.round(((scale[j][1]-mousePos.y+300)/scale[j][0])*op)/op + "; ";
     }
   }

   YY = parseInt(steelData[2].substr(0,4),10);
   MM = parseInt(steelData[2].substr(5,2),10);
   DD = parseInt(steelData[2].substr(8,2),10);
   hh = parseInt(steelData[2].substr(11,2),10);
   mm = parseInt(steelData[2].substr(14,2),10);
   ss = parseInt(steelData[2].substr(17,2),10);

   ss= ss + mousePos.x;
   day = Math.floor(ss/86400);
   hour = Math.floor(ss/3600)-(day*86400);
   minutes = Math.floor(ss/60)-(day*86400)-(hour*60);
   seconds = ss-(day*86400)-(hour*3600)-(minutes*60);
   
   mm = mm + Math.floor(ss/60);
   day = Math.floor(mm/1440);
   hour = Math.floor(mm/60)-(day*1440);
   minutes = mm-(day*1440)-(hour*60);

   hh = hh + Math.floor(mm/60);
   day = Math.floor(hh/24);
   hour = hh-(day*24);

   DD = DD + Math.floor(hh/24);
   day = DD;

   if (MM < 10) {MMS = "0"+MM;} else {MMS = MM;}
   if (day < 10) {dayS = "0"+day;} else {dayS = day;}
   if (hour < 10) {hourS = "0"+hour;} else {hourS = hour;}
   if (minutes < 10) {minutesS = "0"+minutes;} else {minutesS = minutes;}
   if (seconds < 10) {secondsS = "0"+seconds;} else {secondsS = seconds;}
   tit = tit + " Время: "+YY+"-"+MMS+"-"+dayS+" "+ hourS + ":" + minutesS + ":" + secondsS;
   mouseTime = YY+"-"+MMS+"-"+dayS+" "+ hourS + ":" + minutesS + ":" + secondsS;
   var mouse = document.getElementById("mouse");
   mouse.textContent = "Положение курсора мыши: " + tit;

   mouseX1 = mousePos.x;
   mouseY1 = mousePos.y;
   plotGraph();
   
 }, false);
//-----------------------------------------------------------------------------
doc2.addEventListener('mousemove', function(evt) {
   var mousePos = getMousePos(doc2, evt);
   mouseX = mousePos.x;
   mouseY = mousePos.y;
 }, false);
//-----------------------------------------------------------------------------
doc2.addEventListener('click', function() {

  k = 0;
  dx = 0;
  var m = localData.length;
  if (m <= 0) {m = localDataC.length;}
  for (var i = 0; i < m; i++) {
    if ((mouseX > 5+dx*120) && (mouseX < 5+dx*120+115) && (mouseY > k*50+5) && (mouseY < k*50+5+40))
    {
       checkElem[i].checked = !checkElem[i].checked;
       plotGraph();
       break;
    }
      k = k + 1;
      if (k >= 10)
      {
        k = 0;
        dx = dx + 1
      }
   }
 

 }, false);
//-----------------------------------------------------------------------------
function onClickCheck()
{
  for (var i = 0; i < checkElem.length; i++) {
    checkElem[i].addEventListener('click', function() {
      plotGraph();
    }, false);
  }
}
//-----------------------------------------------------------------------------
function include(url)
{
  var oldScript = document.getElementById("dataLine");
  var can = document.body;

  var newScript = document.createElement('script');
  newScript.src = url;
  newScript.type= "text/javascript";

  can.insertBefore(newScript, oldScript);
  can.removeChild(oldScript);

  newScript.id="dataLine";
}
//-----------------------------------------------------------------------------
//-----------------------------------------------------------------------------
CreateElement();
onClickCheck();
plotGraph();
scrollPos.scrollTop = 300;
//var k = 0;

var timerId = setInterval(function() {
//     k += 1;
     include('line.js')// url
     plotGraph();
//     if (k === 600) {
//        clearInterval(timerId);
//     }
}, 1000);