var listElsort = [21,0,2,1,7,9,6,4,3,5,8,12,11,10,13,17,19,14,16,15,18,20];
var listEl = ["C","Si","Mn","P","S","Al","Cu","Cr","Mo","Ni","V","Ti","Nb","Ca","Co","W","B","As","Sn","N","Cэ","T, °C"];

var el = document.getElementById("el");
var elLab = document.getElementById("elLab");
var elMin = document.getElementById("min");
var elMax = document.getElementById("max");
var elTar = document.getElementById("target");
var elMod = document.getElementById("model");

var minElem = [];
var maxElem = [];
var tarElem = [];
var modElem = [];

var timeMod = document.getElementById("time");

var timeSort = true;
var timeSortTd = document.getElementById("timeSort");

var timeSortAd = true;
var timeSortTdAd = document.getElementById("timeSortAd");

var timeSortT = true;
var timeSortTdT = document.getElementById("timeSortT");
//--------------------------------------------------------------------------------
function CreateElement()
{
  elLab.style.borderColor ="white";
  for (var i = 0; i < listEl.length; i++)
  {
    var newElement = document.createElement('td');
    el.appendChild(newElement);
    newElement.textContent = listEl[listElsort[i]];
    newElement.style.backgroundColor = "skyblue";

    //if (i < listEl.length - 1) {
    newElement = document.createElement('td');
    elLab.appendChild(newElement);
    newElement.textContent = listEl[listElsort[i]];
    newElement.style.backgroundColor = "skyblue";
    //}  
  
    newElement = document.createElement('td');
    elMin.appendChild(newElement);
    newElement.textContent = "";
    minElem[i] = newElement;
  
    newElement = document.createElement('td');
    elMax.appendChild(newElement);
    newElement.textContent = "";
    maxElem[i] = newElement;
  
    newElement = document.createElement('td');
    elTar.appendChild(newElement);
    newElement.textContent = "";
    newElement.style.backgroundColor = "lightsalmon";
    tarElem[i] = newElement;
  
    newElement = document.createElement('td');
    elMod.appendChild(newElement);
    newElement.textContent = "";
    modElem[i] = newElement;

  }
}
//--------------------------------------------------------------------------------
function AddLab(tab,j,posAn)
{
      var newTr = document.createElement('tr');

      var tit = "";
      if (j === posAn) {tit = "Анализ";}
      var newEl = document.createElement('td');      
      newTr.appendChild(newEl);
      newEl.textContent = tit;
      newEl.style.backgroundColor = "lightyellow";
      newEl.style.fontWeight = "bold";

      var newEl = document.createElement('td');      
      newTr.appendChild(newEl);
      newEl.textContent = timePointR[j];
      newEl.style.backgroundColor = "lightyellow";

      var newEl = document.createElement('td');      
      newTr.appendChild(newEl);
      newEl.textContent = "";
      newEl.style.backgroundColor = "lightyellow";

      for (var i = 0; i < plotPointR.length; i++) {
        var newEl = document.createElement('td');
        newTr.appendChild(newEl);
        newEl.textContent = plotPointR[listElsort[i+1]][j];
        newEl.style.backgroundColor = "lightyellow";
        newEl.style.color = "black";
        newEl.style.fontWeight = "normal";
        
        if (localData.length > 0) {
          var maxTmp = localData[listElsort[i+1]+1][3];
          if (maxTmp < 0) {maxTmp = 1000;}
          var minTmp = localData[listElsort[i+1]+1][2]; }
        
          if ((plotPointR[listElsort[i+1]][j] >= minTmp) && (plotPointR[listElsort[i+1]][j] <= maxTmp))
          {
            newEl.style.backgroundColor = "lightyellow";
          }
          else {
            if (plotPointR[listElsort[i+1]][j] < minTmp) {newEl.style.backgroundColor = "deepskyblue";}
            if (plotPointR[listElsort[i+1]][j] > maxTmp) {newEl.style.backgroundColor = "orange";}
            //newEl.style.backgroundColor = "orange";//"lime";
            //newEl.style.color = "crimson";//"purple";
            newEl.style.fontWeight = "bold";
          }
      // newEl.width = "50";
      }
      tab.appendChild(newTr);
}
//--------------------------------------------------------------------------------
function PrintP()
{
    //var tab = document.getElementById("tabEl");
    var tab = document.getElementById("labEl");
    var m = tab.children.length - 1;
    //var tmp = document.getElementById("meltNum");
    //tmp.textContent = m
    if (m > 0) {
      for (var i = m; i > 0; i--){
        var div = tab.children[i];
        tab.removeChild(div);
      }
    }

    //анализы
    if (timeSort === true)
    {
      for (var j = timePointR.length-1; j >= 0; j--) {
        AddLab(tab,j,timePointR.length-1);
      }
    }
    else {
      for (var j = 0; j < timePointR.length; j++) {
        AddLab(tab,j,0);
      }
    }
}
//--------------------------------------------------------------------------------
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
//--------------------------------------------------------------------------------
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

    if (timeSortAd === true)
    {
      for (var j = additive.length-1; j >= 0; j--) {
        massa = AddAdd(tab,j,massa);
      }
    }
    else {
      for (var j = 0; j < additive.length; j++) {
        massa = AddAdd(tab,j,massa);
      }
    }

    var newTr = document.createElement('tr');    

    var newEl = document.createElement('td');      
    newTr.appendChild(newEl);
    newEl.textContent = "Всего:";
    newEl.style.backgroundColor = "skyblue";
    //newEl.style.fontWeight = "bold";
    newEl.setAttribute("colspan","3",0);

    var newEl = document.createElement('td');      
    newTr.appendChild(newEl);
    newEl.textContent = massa;
    newEl.style.backgroundColor = "skyblue";
    newEl.classList.add('tright');
    //newEl.style.fontWeight = "bold";
      
    tab.appendChild(newTr);
}
//--------------------------------------------------------------------------------
function AddT(tab,i)
{
      var newTr = document.createElement('tr');

      var newEl = document.createElement('td');      
      newTr.appendChild(newEl);
      newEl.textContent = tempPoint[i][3];

      var newEl = document.createElement('td');      
      newTr.appendChild(newEl);
      newEl.textContent = tempPoint[i][2];
      newEl.classList.add('tc');

      var newEl = document.createElement('td');      
      newTr.appendChild(newEl);
      if (tempPoint[i][4] >= 0) {newEl.textContent = tempPoint[i][4];}
      else {newEl.textContent = "";}
      newEl.classList.add('tc');      

      tab.appendChild(newTr);
}
//--------------------------------------------------------------------------------
function PrintTemp()
{
    var tab = document.getElementById("temp");
    var m = tab.children.length - 1;
    
    if (m > 0) {
      for (var i = m; i > 0; i--){
        var div = tab.children[i];
        tab.removeChild(div);
      }
    }
    if (timeSortT === true)
    {
      for (var i = tempPoint.length-1; i >= 0; i--) {
        AddT(tab,i);
      }
    }
    else
    {
      for (var i = 0; i < tempPoint.length; i++) {
        AddT(tab,i);
      }
    }    
}
//--------------------------------------------------------------------------------
function printNowTime()
{
  if (nowTime.length > 0)
  {
      //время
      var t = document.getElementById("nowTime");
      t.textContent = " Текущее время: " + nowTime[0];
      t = document.getElementById("meltTime");
      t.textContent = " Продолжительность плавки: " + nowTime[1];
  }
  else {
      var t = document.getElementById("nowTime");
      t.textContent = " Текущее время: ";
      t = document.getElementById("meltTime");
      t.textContent = " Продолжительность плавки: ";
  }
}
//--------------------------------------------------------------------------
function PrintM()
{
  var dat = document.getElementById("meltNum");
  dat.textContent = "Номер плавки: " + steelData[1];
  dat = document.getElementById("steelMk");
  dat.textContent = "Марка стали: " + steelData[0];
  dat = document.getElementById("startTime");
  dat.textContent = "Время начала плавки: " + steelData[2];
  dat = document.getElementById("liquidus");
  dat.textContent = "Температура ликвидуса: " + steelData[3] +"°C";

  printNowTime();

  if (plotTime.length > 0) {
    timeMod.textContent = plotTime[1][plotTime[0].length-1];
  }
  else {
    timeMod.textContent = "";
    for (var i = 0; i < listEl.length; i++) {
      modElem[i].textContent = "";
      modElem[i].style.backgroundColor = "white";
    }
  }

  PrintP();
  //alert('P');
  if (localData.length > 0) {
    var x = plotTime[0][plotTime[0].length-1];
    if (localData[0][1] >= 0) {modElem[0].textContent = localData[0][1];}//+localData[i][0];}
    else {modElem[0].textContent = "";}
    for (var i = 1; i < localData.length; i++) {
      modElem[i].textContent = "";
      modElem[i].style.backgroundColor = "white";

      if (startTime > 0) {
        if (x >= startTime && localData[listElsort[i]+1][1] >= 0) {modElem[i].textContent = localData[listElsort[i]+1][1];}//+localData[i][0];}
        if (localData[listElsort[i]+1][4] === 1 && x >= startTime) {modElem[i].style.backgroundColor = "yellow";}
      }
      if (localData[listElsort[i]+1][2] >= 0 && i > 0) {minElem[i].textContent = localData[listElsort[i]+1][2];} else {minElem[i].textContent = "";}//+localData[i][0]
      if (localData[listElsort[i]+1][3] >= 0 && i > 0) {maxElem[i].textContent = localData[listElsort[i]+1][3];} else {maxElem[i].textContent = "";}//+localData[i][0]
      if (localData[listElsort[i]+1][5] >= 0 && i > 0) {tarElem[i].textContent = localData[listElsort[i]+1][5];} else {tarElem[i].textContent = "";}//+localData[i][0]
    }
//    if (startTime > 0) {
//      if (x >= startTime) {modElem[modElem.length-1].textContent = localData[0][1];}//+localData[i][0];}
//    }
//    if (localData[0][1] > 0) {modElem[modElem.length-1].textContent = localData[0][1];}//+localData[i][0];}
//    else {modElem[modElem.length-1].textContent = "";}
  }

  PrintAdd();
  PrintTemp();
}
//--------------------------------------------------------------------------------
function include(url,elID)
{
  var oldScript = document.getElementById(elID);
  var can = document.body;

  var newScript = document.createElement('script');
  newScript.src = url;
  newScript.type= "text/javascript";

  can.insertBefore(newScript, oldScript);
  can.removeChild(oldScript);

  newScript.id=elID;
}
//--------------------------------------------------------------------------------
function PrintAll()
{
  PrintM();
  var timerId = setInterval(function() {
    include('http://test-anaconda.chtpz.ru:5005/line.js','dataLine');// url
    PrintM();
  }, 1000);
}
//--------------------------------------------------------------------------------
timeSortTd.addEventListener('click', function() {
  if (timeSort === true)
  {
    timeSort = false;
    timeSortTd.textContent = "Время ˅";
  }
  else
  {
    timeSort = true;
    timeSortTd.textContent = "Время ˄";
  }
  PrintP();
 }, false);
//--------------------------------------------------------------------------------
timeSortTdAd.addEventListener('click', function() {
  if (timeSortAd === true)
  {
    timeSortAd = false;
    timeSortTdAd.textContent = "Время ˅";
  }
  else
  {
    timeSortAd = true;
    timeSortTdAd.textContent = "Время ˄";
  }
  PrintAdd();
 }, false);
//--------------------------------------------------------------------------------
timeSortTdT.addEventListener('click', function() {
  if (timeSortT === true)
  {
    timeSortT = false;
    timeSortTdT.textContent = "Время ˅";
  }
  else
  {
    timeSortT = true;
    timeSortTdT.textContent = "Время ˄";
  }
  PrintTemp();
 }, false);
//--------------------------------------------------------------------------------
CreateElement();
PrintAll();