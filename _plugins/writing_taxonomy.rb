# Use declared subjects, rather than historical folder names, for classification.
# Articles live in root _posts; explicit permalinks preserve the existing archive.
require 'kramdown'
require 'kramdown-parser-gfm'

module Jekyll
  class WritingTaxonomy < Generator
    priority :highest

    def generate(site)
      taxonomy = site.data.fetch('taxonomy')
      site.posts.docs.each do |post|
        text = File.read(post.path)
        front = text.match(/\A---\s*\n(.*?)\n---\s*\n/m)
        metadata = front ? SafeYAML.load(front[1]) : {}
        categories = metadata.fetch('categories', [])
        categories = categories.split if categories.is_a?(String)
        unknown = categories - taxonomy.keys
        raise Errors::FatalException, "Unknown categories in #{post.relative_path}: #{unknown.join(', ')}" unless unknown.empty?
        post.data['categories'] = categories

        headings = []
        visit = lambda do |node|
          headings << node.options[:raw_text] if node.type == :header
          node.children.each { |child| visit.call(child) }
        end
        visit.call(Kramdown::Document.new(post.content, :input => 'GFM').root)
        post.data['search_headings'] = headings.compact.join(' ')
        post.data['search_subjects'] = categories.map do |category|
          entry = taxonomy.fetch(category)
          [entry['label'], entry['aliases']].compact.join(' ')
        end.join(' ')
      end
    end
  end
end
