(function ($) {

    var row_index = 1;
    var KEEP_ASIDE_COOKIE_NAME = "smetisufod-keep-aside";
    var COOKIE_SEP = " - ";

    $(function(){
        $("#template-row").hide();
        
        $("#add-row").click(function() {
            addAttributeRow();
        });
        
        $(document).on("click", ".remove-row", function() {
            $(this).parent().remove();
            applyEffectRowStyle();
        });
        
        $("#advanced-search").hide();
        $("#switch-advanced-search").click(function() {
            $("#advanced-search").toggle();
        });
        
        $("#clear-search").click(function() {
            $("input:text").val("");
            $(".craft-case").removeProp("checked");
            $(".effect").remove();
        });
        
        $("#search").click(function() {
            $("#search-form").submit();
        });
        
        $(document).on("keypress", "#search-form input[type='text']", function(event) {
            if (event.keyCode == 13) {
                $("#search").click();
            }
        });
        
        
        setFormFromUrlParameters();
        makeCheckboxTree();
        
        $(".item-lookup").lookupitem();
        
        
        $("#aside-items").hide();
        
        $(document).on("click", "#aside-items .remove-row", function() {
            var currentItems = $.cookie(KEEP_ASIDE_COOKIE_NAME);
            if (!currentItems) {
                return;
            }
            
            currentItems = currentItems.split(COOKIE_SEP);
            
            var index = undefined;
            var element = $(this);
            $.each(currentItems, function(i, e) {
                if (e == element.attr("name")) {
                    index = i;
                }
            });
            
            if (index !== undefined) {
                currentItems.splice(index, 1);
            }
            currentItems.join(COOKIE_SEP);
            
            $.cookie(KEEP_ASIDE_COOKIE_NAME, currentItems);
            
            reloadAsideItemsFromCookie();
        });
        
        $(document).on("click", ".keep-aside", function() {
            var currentItems = $.cookie(KEEP_ASIDE_COOKIE_NAME);
            
            if (isItemInCookie($(this).attr("name"))) {
                return;
            }
            
            if (currentItems) {
                currentItems += COOKIE_SEP + $(this).attr("name");
            } else {
                currentItems = $(this).attr("name");
            }
            
            $.cookie(KEEP_ASIDE_COOKIE_NAME, currentItems);
            
            reloadAsideItemsFromCookie();
        });
        
        $("#remove-aside").click(function() {
            $.removeCookie(KEEP_ASIDE_COOKIE_NAME);
            reloadAsideItemsFromCookie();
        });
        
        reloadAsideItemsFromCookie();
        
        $(document).on("click", ".invalid > a", function() {
            var self = $(this)
            $.get("flag_invalid", {"name": self.attr("name")}, function(result) {
                var parent = self.parent();
                parent.find("a").hide();
                parent.find("span").show();
            });
        });
    });

    function setFormFromUrlParameters() {
        var paramString = unescape(decodeURIComponent(window.location.search.substring(1)));
        var params = paramString.split('&');
        
        if (params.length == 0 || !params[0]) {
            addAttributeRow();
            $("#types :checkbox[name='type']").prop("checked", "checked");
            $("#include-panoplie").prop("checked", "checked");
            return;
        }
        
        var isTypeDefined = false;
        
        $.each(params, function(i, param) {
            var key = param.split("=")[0].replace("+", " ", "g");
            var value = param.split("=")[1].replace("+", " ", "g");
            
            switch (key) {
                case "level-min":
                case "level-max":
                case "name":
                case "cost-min":
                case "cost-max":
                case "range-min":
                case "range-max":
                    $("#"+key).val(value);
                    break;
                    
                case "type":
                    isTypeDefined = true;
                    value = value.replace(" ", "", "g");
                    $("#type-"+value).prop("checked", "checked");
                    break;
                case "include-panoplie":
                    $("#"+key).prop("checked", "checked");
                    break;
                case "recipe":
                    $("#recipe-"+value).prop("checked", "checked");
                    break;
                default:
                    if (key.startsWith("attribute-") || key.startsWith("value-")) {
                        var index = key.slice(key.lastIndexOf("-")+1)
                        addAttributeRow(index);
                        $("#"+key).val(value);
                    }
                    break;
            }
        });
        
        if (!isTypeDefined) {
            $("#types :checkbox[name='type']").prop("checked", "checked");
        }
        
        $(".category").each(function() {
            if ($(this).find("[name='type']:checkbox:checked").length != 0 && $(this).find("[name='type']:checkbox:not(:checked)").length != 0) {
                $(this).removeClass("tree-collapsed").addClass("tree-expanded");
            }
        });
        
        if ($("#advanced-search").find(":checked").length != 0 || $("#advanced-search").find("input:text").filter(function(){return $.trim($(this).val()).length > 0;}).length != 0) {
            $("#advanced-search").show();
        }
    }

    function addAttributeRow(index) {
        if (index) {
            row_index = index;
            if ($("#attribute-"+row_index).length != 0) {
                return;
            }
        } else {
            while ($("#attribute-"+row_index).length != 0) {
                row_index++;
            }
            index = row_index;
            row_index++;
        }
        
        var row = $("#template-row").clone();
        row.removeAttr("id")
            .addClass("effect")
            .show();
        
        var select = row.find("select");
        var name = select.attr("name") + "-" + index;
        select.attr("name", name).attr("id", name);
        
        var minValue = row.find("input:text[name='value-min']");
        name = minValue.attr("name") + "-" + index;
        minValue.attr("name", name).attr("id", name);
        
        var maxValue = row.find("input:text[name='value-max']");
        name = maxValue.attr("name") + "-" + index;
        maxValue.attr("name", name).attr("id", name);
        
        $("#effects").append(row);
        
        applyEffectRowStyle();
    }
    
    function applyEffectRowStyle() {
        $("#effects > li").each(function(i, e) {
            $(e).removeClass("even odd");
            if (i % 2 == 1) {
                $(e).addClass("even");
            } else {
                $(e).addClass("odd");
            }
        });
    }

    function makeCheckboxTree() {
        $("#types li").click(function(event) {
            if (event.target == $(this)[0] && $(this).find("ul").length) {
                $(this).toggleClass("tree-expanded tree-collapsed");
                return false;
            }
        });
        
        $("#types :checkbox").change(function() {
            checkChildren($(this));
            checkParent($(this));
        });
        
        $("#types :checkbox[name='type']").change();
    }

    function checkChildren(element) {
        if ($(element).prop("checked")) {
            $(element).parent().find(":checkbox").prop("checked", "checked");
        } else {
            $(element).parent().find(":checkbox").removeProp("checked");
        }

    }

    function checkParent(element) {
        var parent = $(element).parent().parent().parent().find(">:checkbox");
        if (parent.length == 0) {
            return;
        }
        
        if ($(element).parent().parent().find(">>:checkbox:not(:checked)").length) {
            parent.removeProp("checked");
        } else {
            parent.prop("checked", "checked");
        }
        
        checkParent(parent);
    }
    
    function reloadAsideItemsFromCookie() {
        var items = $.cookie(KEEP_ASIDE_COOKIE_NAME)
        if (!items) {
            $("#aside-items").hide();
            return;
        }
        
        items = items.split(COOKIE_SEP);
        
        $("#aside-items ul>li").remove();
        
        $.each(items, function(i, e) {
            var row = $("<li>");
            var content = $("<span>", {
                "class": "item-lookup",
            }).html(e);
            
            content.lookupitem();
            row.append(content);
            row.append($("<input>", {
                "type": "button",
                "class": "remove-row",
                "name": e,
            }));
            $("#aside-items ul").append(row);
        });
        
        if (items.length) {
            $("#aside-items").show();
        } else {
            $("#aside-items").hide();
        }
    }
    
    function isItemInCookie(name) {
        var cookie = $.cookie(KEEP_ASIDE_COOKIE_NAME);
        if (!cookie) {
            return false;
        }
        
        if (name == cookie) {
            return true;
        }
        
        var result = false;
        $.each(cookie.split(COOKIE_SEP), function(i, e) {
            if (e == name) {
                result = true;
            }
        });
        
        return result;
    }
    
})(jQuery);