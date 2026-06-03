# frozen_string_literal: true

# Production builds omit unpublished posts, but published posts may still {% link %}
# to them. Jekyll's default link tag aborts the build; this override returns a best-effort
# URL (or "#") so deploy succeeds. Unpublished targets stay absent from site.posts.
module Jekyll
  module Tags
    class TolerantLink < Link
      def render(context)
        super
      rescue ArgumentError => e
        raise unless e.message.include?("Could not find document")

        site = context.registers[:site]
        relative_path = Liquid::Template.parse(@relative_path).render(context).strip
        url = guess_url(relative_path, site)
        Jekyll.logger.warn "Link:", "Skipping missing #{relative_path.inspect}; href=#{url}"
        url
      end

      private

      def guess_url(relative_path, site)
        if (m = relative_path.match(%r{\Asections/science/_posts/(\d{4})-(\d{2})-(\d{2})-(.+)\.md\z}))
          path = "/sections/science/#{m[1]}/#{m[2]}/#{m[3]}/#{m[4]}.html"
          return PathManager.join(site.baseurl, path)
        end

        "#"
      end
    end
  end
end

Liquid::Template.register_tag("link", Jekyll::Tags::TolerantLink)
