require "jekyll/footnotes"

# jekyll-footnotes 1.0 emits inline </li> tags that Kramdown escapes when
# parse_block_html is enabled. Keep block boundaries and avoid converting twice.
class ScientificFootnoteBody < Jekyll::FootnoteBody
  def render(context)
    super.sub(/(<li[^>]*>)/, "\\1\n\n").sub('</li>', "\n\n</li>\n")
  end
end
class ScientificFootnoteList < Jekyll::FootnoteList
  def render(context)
    super.sub('<ol class="footnotelist">', '<ol class="footnotelist" markdown="0">')
  end
end
Liquid::Template.register_tag('fnbody', ScientificFootnoteBody)
Liquid::Template.register_tag('footnotes', ScientificFootnoteList)
