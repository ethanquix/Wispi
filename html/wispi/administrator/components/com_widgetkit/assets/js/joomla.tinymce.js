!function(){window.tinyMCE&&!window.WFEditor&&(void 0==window.jSelectArticle&&(window.jSelectArticle=function(t,i,n,e,o,l){var c="";if(""!==l)var c=' hreflang = "'+l+'"';var r="<a"+c+' href="'+o+'">'+i+"</a>";jInsertEditorText(r,"jform_articletext"),jModalClose()}),tinyMCE.PluginManager.add("jArticleButton",function(t,i){t.addButton("button-2Article",{text:"Article",title:"Article",icon:"none icon-file-add",onclick:function(){var i={title:"Article",url:"index.php?option=com_content&view=articles&layout=modal&tmpl=component",buttons:[{text:"Close",onclick:"close"}],width:800,height:500};t.windowManager.open(i)}})}))}();