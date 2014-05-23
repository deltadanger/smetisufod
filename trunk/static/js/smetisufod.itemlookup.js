

(function ($) {
    $.fn.lookupitem = function(options) {
        var self = this;
        
        var settings = $.extend(true, {}, $.fn.lookupitem.defaults, options );
        
        this.each(function() {
            var element = $(this);
            var cursor = "default";
            var doNotHide = false;
            
            if (element.hasClass("smetisufodified")) {
                return;
            }
            element.addClass("smetisufodified");
            
            if (settings.makeLink) {
                if (!element.is("a")) {
                    element = $("<a>", {
                        "style": "color: inherit; text-decoration:inherit;"
                    });
                    element.html($(this).html());
                    $(this).html("");
                    $(this).append(element);
                }
                element.attr("href", "/search.html?include-panoplie=on&name=" + element.html());
                cursor = "pointer";
            }
            
            if (settings.applyStyle) {
                element.css(settings.style);
            }
            
            element.mouseover(function() {
                doNotHide = element.html();
                
                var displayDiv = $("#"+getIdFromItemName(element.html()));
                
                if (displayDiv.length == 0) {
                    var displayDiv = $("<div>", {
                        "id": getIdFromItemName(element.html()),
                        "class": "smetisufod-item-lookup",
                        "style": "position: absolute; margin: 10px",
                    });
                }
                
                $("body").append(displayDiv);
            
                displayDiv.mouseover(function() {
                    doNotHide = element.html();
                });
                
                displayDiv.mouseout(function() {
                    if (doNotHide == element.html()){
                        doNotHide = "";
                    }
                    setTimeout(function() {
                        if (doNotHide != element.html()) {
                            displayDiv.hide();
                        }
                    }, 200);
                });
                
                
                if (!displayDiv.html()) {
                    element.css("cursor", "progress");
                    
                    $.get("get_item", {"name": element.html()}, function(result) {
                        if (result.html) {
                            displayDiv.html(result.html);
                            displayDiv.find(".item-lookup").lookupitem();
                            moveDiv(displayDiv, element);
                        } else {
                            displayDiv.remove();
                        }
                        
                    }).complete(function() {
                        element.css("cursor", cursor);
                    });
                }
                
                displayDiv.show();
                
                moveDiv(displayDiv, element);
            });
            
            element.mouseout(function() {
                if (doNotHide == element.html()){
                    doNotHide = "";
                }
                setTimeout(function() {
                    if (doNotHide != element.html()) {
                        $("#"+getIdFromItemName(element.html())).hide();
                    }
                }, 200);
            });
        });
        
        return this;
    };
    
    $.fn.lookupitem.defaults = {
        applyStyle: true,
        style: {
            "background-color": "#F6EDDC",
            "border": "1px dashed #5E4911",
            "color": "#5E4911",
            "display": "block",
            "margin": "1px",
            "padding": "2px 5px",
            "text-decoration": "none",
        },
        makeLink: false
    };
    
    function getIdFromItemName(name) {
        return name.toLowerCase().replace(" ", "-", "g").replace("'", "", "g");
    }
    
    function moveDiv(displayDiv, element) {
        displayDiv.position({
            "my": "top",
            "at": "center bottom+15px",
            "of": element,
            "collision": "flipfit",
        });
    }
    
}( jQuery ));
