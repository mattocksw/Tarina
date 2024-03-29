import Vue from 'vue'
import Vuex from 'vuex'

Vue.use(Vuex)

function getEditorIndex(editors, category, item) {
    for (var i = 0; i < editors.length; i++) {
        if (editors[i].category === category && editors[i].item === item)
            return i
    }
    return -1
}

export default new Vuex.Store({
  state: {
      story_selected: false,
      story_title: "Tarina",
      content: [],
      editors: [],
      selected_editor_index: 0 /*Used for scrolling*/
  },
  mutations: {
      add_category(state, category) {
          Vue.set(state.content, category, [])
      },
      delete_category(state, category) {
          Vue.delete(state.content, category)
      },
      add_item(state, { category, item }) {
          var updated_list = state.content[category]
          updated_list.push(item)
          //delete previous and reset to trigger vue update
          Vue.delete(state.content, category)
          Vue.set(state.content, category, updated_list)
      },
      delete_item(state, { category, item }) {
          var updated_list = state.content[category]
          Vue.delete(updated_list, updated_list.indexOf(item))
          //delete previous and reset to trigger vue update
          Vue.delete(state.content, category)
          Vue.set(state.content, category, updated_list)
      },
      update_items(state, { category, items }) {
          Vue.delete(state.content, category)
          Vue.set(state.content, category, items)
      },
      update_content(state, content) {
          state.content = Object.assign({}, content)
      },
      update_story_selected(state, b) {
          state.story_selected = b
      },
      update_story_title(state, title) {
          state.story_title = title
      },
      add_editor(state, { category, item }) {
          //check that editor does not exist
          var combined = []
          combined["category"] = category
          combined["item"] = item
          state.selected_editor_index = getEditorIndex(state.editors, category, item) //if editor exists, sets the index to that otherwise creates a new
          if (state.selected_editor_index === -1) {
              state.editors.push(combined)
              state.selected_editor_index = state.editors.length - 1
          }

      },
      delete_editor(state, { category, item }) {
          var index = getEditorIndex(state.editors, category, item)
          if (index !== -1)
              Vue.delete(state.editors, index)
      },
      delete_all_editors(state) {
          state.editors = []
      },
      rename_category(state, { category, new_name })
      {
          //change name in content
          var tmp_category_content = state.content[category]
          Vue.delete(state.content, category)
          Vue.set(state.content, new_name, tmp_category_content)

          //change name in all editors
          var tmp_editors = state.editors
          for (var i = 0; i < tmp_editors.length; i++)
          {
              var tmp_editor = tmp_editors[i]
              if (tmp_editor["category"] === category)
              {
                  tmp_editor["category"] = new_name
                  tmp_editors[i] = tmp_editor
              }
          }

          Vue.delete(state.editors)
          Vue.set(state.editors, tmp_editors)

      },
      rename_item(state, { category, item, new_name }) {
          //change name in content
          var tmp_category_content = state.content[category]          
          tmp_category_content[tmp_category_content.indexOf(item)] = new_name
          Vue.delete(state.content, category)
          Vue.set(state.content, category, tmp_category_content)

          

          //if editor exists, change name there too
          var index = getEditorIndex(state.editors, category, item)          
          if (index !== -1) {
              var tmp_editors = state.editors
              var tmp_editor = tmp_editors[index]

              tmp_editor["item"] = new_name
              tmp_editors[index] = tmp_editor

              Vue.delete(state.editors)
              Vue.set(state.editors, tmp_editors)
          }

          
      },
  },
  actions: {

  }
})
