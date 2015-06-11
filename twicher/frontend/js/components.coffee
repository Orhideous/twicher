{createClass, createFactory, DOM} = require 'react'


List = createClass
  displayName: "List"

  render: ->
    DOM.div(
      null,
      "Hello!"
    )

Excerpt = createClass
  displayName: "Excerpt"

  render: ->
    DOM.div(
      null,
      ""
    )

View = createClass
  displayName: "View"

  render: ->
    DOM.div(
      null,
      ""
    )

Preview = createClass
  displayName: "Preview"

  render: ->
    DOM.div(
      null,
      ""
    )


Editor = createClass
  displayName: "Editor"

  render: ->
    DOM.div(
      null,
      ""
    )

module.exports =
  List: createFactory List
  Excerpt: createFactory Excerpt
  View: createFactory View
  Preview: createFactory Preview
  Editor: createFactory Editor
