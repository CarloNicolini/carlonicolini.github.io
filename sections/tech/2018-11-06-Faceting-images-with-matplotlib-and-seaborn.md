
class FacetGridImage(sns.FacetGrid):
    def map(self, *args, **kwargs):
        """Apply a plotting function to each facet's subset of the data.

        Parameters
        ----------
        args : strings
            Column names in self.data that identify variables with data to
            imshow. The data for each variable is passed to imshow in the
            order the variables are specified in the call.

        Returns
        -------
        self : object
            Returns self.

        """
        # If color was a keyword argument, grab it here
        kw_color = kwargs.pop("color", None)

        # Iterate over the data subsets
        for (row_i, col_j, hue_k), data_ijk in self.facet_data():
            
            # If this subset is null, move on
            if not data_ijk.values.size:
                continue

            # Get the current axis
            ax = self.facet_axis(row_i, col_j)
            #print(row_i,col_j,hue_k,data_ijk,ax)
            # Decide what color to plot with
            kwargs["color"] = self._facet_color(hue_k, kw_color)

            # Insert the other hue aesthetics if appropriate
            for kw, val_list in self.hue_kws.items():
                kwargs[kw] = val_list[hue_k]

            # Insert a label in the keyword arguments for the legend
            if self._hue_var is not None:
                kwargs["label"] = utils.to_utf8(self.hue_names[hue_k])

            # Get the actual data we are going to plot with
            
            plot_data = data_ijk[list(args)]
            if self._dropna:
                plot_data = plot_data.dropna()
            plot_args = [v for k, v in plot_data.iteritems()]

            # Draw the plot
            # self._facet_plot(func, ax, plot_args, kwargs)
            # CARLO Here we do a simple HACK to plot imshow data
            ax.imshow(data_ijk[list(args)].values[0][0])
            ax.grid(False)

        # Finalize the annotations and layout
        self._finalize_grid(args[:2])

        return self

