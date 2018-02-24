    function onClickToToggleCrashDivVisibilityById(button, crashDivId, highlightButtonId, anchorLinkId){

        visibility = button.getAttribute("visibility");
        visibleInnerHTML = button.getAttribute("visibleInnerHTML");
        invisibleInnerHTML = button.getAttribute("invisibleInnerHTML");

        crashDiv = document.getElementById(crashDivId);
        anchorLink = document.getElementById(anchorLinkId);

        highlightStatus = document.getElementById(highlightButtonId).getAttribute("highlightStatus");

        // 隐藏
        if(visibility == "visible"){
            crashDiv.setAttribute("hidden", "hidden");
            button.setAttribute("visibility", "invisible");
            button.innerHTML = invisibleInnerHTML;
            if(highlightStatus == "on"){
                anchorLink.style="color:red;font-weight:normal";
            } else if(highlightStatus == "off"){
                anchorLink.style="color:blue;font-weight:normal";
            }
        }
        // 显示
        else if(visibility == "invisible"){
            crashDiv.removeAttribute("hidden");
            button.setAttribute("visibility", "visible");
            button.innerHTML = visibleInnerHTML;
            if(highlightStatus == "on"){
                anchorLink.style="color:red;font-weight:bold";
            } else if(highlightStatus == "off"){
                anchorLink.style="color:blue;font-weight:bold";
            }
        }
    }

    function onClickToToggleCrashDivHightlightById(button, crashDivId, visibilityButtonId, anchorLinkId){

        highlightStatus = button.getAttribute("highlightStatus");
        highlightOnInnerHTML = button.getAttribute("highlightOnInnerHTML");
        highlightOffInnerHTML = button.getAttribute("highlightOffInnerHTML");

        crashDiv = document.getElementById(crashDivId);
        anchorLink = document.getElementById(anchorLinkId);

        visibility = document.getElementById(visibilityButtonId).getAttribute("visibility");

        // 高亮
        if(highlightStatus == "off"){
            button.setAttribute("highlightStatus", "on");
            button.innerHTML = highlightOnInnerHTML;
            crashDiv.style="color:red";
            if(visibility == "visible"){
                anchorLink.style="color:red;font-weight:bold";
            } else if(visibility == "invisible"){
                anchorLink.style="color:red;font-weight:normal";
            }
        }
        // 去掉高亮
        else if(highlightStatus == "on"){
            button.setAttribute("highlightStatus", "off");
            button.innerHTML = highlightOffInnerHTML;
            crashDiv.style="color:black";
            if(visibility == "visible"){
                anchorLink.style="color:blue;font-weight:bold";
            }else if(visibility == "invisible"){
                anchorLink.style="color:blue;font-weight:normal";
            }
        }
    }

    function onClickToToggleElementsVisibilityByClassName(button, className){

        visibility = button.getAttribute("visibility");
        visibleInnerHTML = button.getAttribute("visibleInnerHTML");
        invisibleInnerHTML = button.getAttribute("invisibleInnerHTML");

        elements = document.getElementsByClassName(className);

        // 隐藏
        if(visibility == "visible"){
            var i;
            for(i = 0; i < elements.length; i++){
                elements[i].setAttribute("hidden", "hidden");
            }
            button.setAttribute("visibility", "invisible");
            button.innerHTML = invisibleInnerHTML;
        }
        // 显示
        else{
            var i;
            for(i = 0; i < elements.length; i++){
                elements[i].removeAttribute("hidden");
            }
            button.setAttribute("visibility", "visible");
            button.innerHTML = visibleInnerHTML;
        }

    }

function onVersionNameCheckBoxClicked(checkBox){
    for(i = 1; i < arguments.length; i++){
        strCrashOrder = arguments[i];
        buttonToggleCrashVisibility = document.getElementById("button_visibility_" + strCrashOrder);
        onClickToToggleCrashDivVisibilityById(buttonToggleCrashVisibility, strCrashOrder, "anchorLink_" + strCrashOrder);
    }
}