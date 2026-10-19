# Do not expose legacy documentation links when their files were absent at source.
module ResourceLinks
  def available_resource(value)
    return false if value.nil? || value.empty?
    return true if value.match?(%r{\Ahttps?://})
    site = @context.registers[:site]
    File.file?(File.join(site.source, value.delete_prefix('/')))
  end
end
Liquid::Template.register_filter(ResourceLinks)
