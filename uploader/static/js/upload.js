/**
 * Created by alex on 14.05.15.
 */
$(function () {

    function rerenderTable() {
        $.get("/upload/list/", function (data) {
            var table = $(".image-list-table");
            table.find("tr").remove();
            table.append(data);
        });
    }

    $('#fileupload').fileupload({
        formData: function (form) {
            var data = form.serializeArray();
            data.push(
                {"name": "name", "value": this.files[0]["filename_to_upload"]}
            );
            return data;
        },
        url: '.',
        dataType: 'json',
        add: function (e, data) {
            var $this = $(this);

            data
                .process(function () {
                    return $this.fileupload('process', data);
                })
                .always(function () {
                    renderPreviewTable(data, this.element.form);
                });
        },
        done: function (e, data) {
            rerenderTable();
        }

    });
    renderPreviewTable = function (data, form) {
        var that = this
            , tr = $("<tr>")
            , table = $('#files-to-upload')
            , file = data.files[0]
            , button = $("<button class='btn btn-primary start'><i class='glyphicon glyphicon-upload'></i></button>")
                .on("click", function () {
                    data.files[0]["filename_to_upload"] = $(this).closest("tr").find("input.filename").val();
                    button
                        .find("i")
                        .removeClass("glyphicon-upload")
                        .addClass("glyphicon-hourglass")
                        .append("<span>Uploading...</span>");
                    data.submit()
                        .success(function () {
                            button
                                .removeClass("btn-primary")
                                .addClass("btn-success")
                                .find("i")
                                .removeClass("glyphicon-hourglass")
                                .addClass("glyphicon-ok");
                            tr.fadeOut("slow", function () {
                                $(this).remove();
                            });
                        })
                        .error(function (jqXHR, textStatus, errorThrown) {
                            var isRequestError = jqXHR.status == 400
                                , message = $('<div class="alert alert-danger" role="alert">'
                                + '<strong>'
                                + (isRequestError ? "Request error! " : "Unknown error!")
                                + '</strong>'
                                + (isRequestError ? jqXHR.responseJSON["__all__"][0] : "")
                                + '</div>');
                            tr.find("button").remove();
                            tr.last("td").append(message);
                        });
                })
            , slugField = $("<input type='text' class='form-control filename'/>").val(file.name);
        tr
            .append($("<td>").append(file.preview))
            .append($("<td>").append(file.name))
            .append($("<td>").append((file.size / 1024).toFixed(1) + " Килобайт"))
            .append($("<td>").append(slugField))
            .append($("<td>").append(button))
            .appendTo(table)
    };
    $(".image-list-table").on("click", "button.delete", function () {
        var $this = $(this);
        $.ajax({
            type: "POST",
            url: $this.data("url"),
            beforeSend: function (xhr, settings) {
                if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
                    xhr.setRequestHeader("X-CSRFToken", $.cookie('csrftoken'));
                }
            },
            success: function () {
                rerenderTable();
            }
        });
    });
    function csrfSafeMethod(method) {
        return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
    }

});
