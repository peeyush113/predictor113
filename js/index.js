/**
 * Created by penguin on 11/12/13.
 */

$(document).ready(function(){
    $("input:radio[name='jobSeeker']").change(function(){
        var selectedJobSeeker = $("input:radio[name='jobSeeker']:checked");
        $('.success').removeClass('success');
        selectedJobSeeker.parent('td').addClass('success');
        selectedJobSeeker.parent('td').next('td').addClass('success');
        selectedJobSeeker.parent('td').prev('td').addClass('success');
        $.ajax({
            url: '/getSuggest',
            data: {
                selectedId: selectedJobSeeker.val()
            },
            type: "POST",
            success: function(response){
                var suggestedProvider = $.parseJSON(response);
                var suggestedProviderDiv = $("#suggestedProvider");
                suggestedProviderDiv.html('');
                var html = "<h2>suggested job provider in descending order of rank</h2><table class='table table-hover'><tr><th>#</th><th>suggested job provider</th><td>Rank</td></tr>";
                for(providerIndex in suggestedProvider[0]){
                    id = "#jobProvider_"+(suggestedProvider[0][providerIndex]+1);
                    $(id).parent('td').addClass('success');
                    $(id).parent('td').next('td').addClass('success');
                    html = html + "<tr><td>"+(suggestedProvider[0][providerIndex]+1)+"</td><td>"+$(id).parent('td').next('td').text()+"</td><td>"+suggestedProvider[1][providerIndex]+"</td></tr>"
                }
                html = html+"</table>";
                suggestedProviderDiv.html(html);
            },
            fail: function(){
                alert("sorry!!")
            }
        })
    });
});
