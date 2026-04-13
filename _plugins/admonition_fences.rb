# frozen_string_literal: true

# MyST / MDX-style fenced admonitions for Kramdown:
#
#   :::note
#   Body supports **markdown**.
#   :::
#
# Inner content is parsed via kramdown's `markdown="1"` on the `<aside>`.
module Jekyll
  module AdmonitionFences
    # Opening fence at start of file or after a newline; closing `:::` on its own line.
    # /m so ^ matches after each newline; no /x (whitespace in pattern is literal).
    BLOCK = %r{(?:\A|\n):::(\w[-\w]*)\s*\n(?<body>[\s\S]*?)^:::\s*(?:\n|\z)}m

    module_function

    def transform(content)
      return content unless content.is_a?(String) && content.include?(":::")

      content.gsub(BLOCK) do
        type = Regexp.last_match(1).downcase.gsub(/[^a-z0-9-]/, "")
        type = "note" if type.empty?
        body = Regexp.last_match(:body)
        %(<aside class="admonition admonition--#{type}" markdown="1">\n#{body}</aside>\n)
      end
    end
  end
end

Jekyll::Hooks.register %i[documents pages], :pre_render do |doc, _payload|
  path = doc.path
  next unless path&.match?(/\.(md|markdown)\z/i)

  doc.content = Jekyll::AdmonitionFences.transform(doc.content)
end
