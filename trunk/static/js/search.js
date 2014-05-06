(function ($) {

    var row_index = 1;

    $(function(){
        $("#template-row").hide();
        
        $("#add-row").click(function() {
            addAttributeRow();
        });
        
        $(document).on("click", ".remove-row", function() {
            $(this).parent().remove();
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
        
        setFormFromUrlParameters();
        makeCheckboxTree();
    });

    function setFormFromUrlParameters() {
        var paramString = unescape(decodeURIComponent(window.location.search.substring(1)));
        var params = paramString.split('&');
        
        if (params.length == 0 || !params[0]) {
            addAttributeRow();
            $("#types :checkbox[name='type']").prop("checked", "checked");
            return;
        }
        
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
                    if (key.startsWith("attribute-")) {
                        var row = addAttributeRow();
                        row.find("select").val(value);
                        
                    } else if (key.startsWith("value-")) {
                        $("#"+key).val(value);
                    }
                    break;
            }
        });
        
        $(".category").each(function() {
            if ($(this).find("[name='type']:checkbox:checked").length != 0 && $(this).find("[name='type']:checkbox:not(:checked)").length != 0) {
                $(this).removeClass("tree-collapsed").addClass("tree-expanded");
            }
        });
    }

    function addAttributeRow() {
        var row = $("#template-row").clone();
        row.removeAttr("id")
            .addClass("effect")
            .show();
        
        var select = row.find("select");
        select.attr("name", select.attr("name") + "-" + row_index);
        
        var minValue = row.find("input:text[name='value-min']");
        minValue.attr("name", minValue.attr("name") + "-" + row_index);
        
        var maxValue = row.find("input:text[name='value-max']");
        maxValue.attr("name", maxValue.attr("name") + "-" + row_index);
        
        row_index++;
        
        $("#effects").append(row);
        return row;
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
})(jQuery);