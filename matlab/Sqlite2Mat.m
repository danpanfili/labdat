%% Main
function [out] = Sqlite2Mat(path, query, trim)
    if nargin < 3;  trim = true;    end

    db          = sqlite(path);     % Open Sqlite Connection
    datatable   = fetch(db, query); % Fetch data from query

    if height(datatable) == 0
        out = [];
        return
    end
    
    if trim;    key     = TrimPrefixes( datatable.key );
    else;       key     = datatable.key;
    end
    
    keymap  = GroupKeys( key );
    out     = Keymap2Struct( keymap, datatable );
    
    db.close() % Close Sqlite Connection
end

%% Remove unused key prefixes
function [key] = TrimPrefixes(key)
    key = split(key,'.');

    idx = [];
    for i = 1:width(key)
        len = length( unique(key(:, i)) );
        
        if len == 1;    idx = [idx, i]; end
    end

    key(:,idx) = [];

    if length(key) > 1;     key = join(key,"."); end
end

%% Group keys that share all but the last character
function [keymap] = GroupKeys(key)
    keyStart    = arrayfun(@(k) extractBefore(k, strlength(k)), key);

    [~,first,~] = unique(keyStart);
    [reps,name] = groupcounts(keyStart);
    
    keymap      = table(name, reps, first);
    oneRep      = keymap.reps == 1;

    keymap.name(oneRep)     = key(keymap.first( oneRep ));
end

%% Convert type
function [data] = ConvertType(data, dtype)
    if      dtype == "float64";     data = typecast(data,'double');
    elseif  dtype == "int64";       data = typecast(data,'int64');
    end
end

%% Correct size
function [data] = FixSize(data, dsize)
    if length(data) == 1
        data = ones(dsize,1) * data;
    end
end

%% Reformat to struct
function [out] = Keymap2Struct(keymap, datatable)
    for k = 1:length( keymap.name )
        row     = keymap( k,: );
        range   = (row.first : row.first + row.reps - 1);
        data    = datatable.data( range );
        dsize   = max(datatable.size( range ));

        dtype   = datatable.dtype( range );
        dtype   = string(mode(categorical(dtype)));

        thisData = [];
        for d = 1:length(data)
            temp = ConvertType(data{d}, dtype);
            temp = FixSize(temp, dsize);
            thisData = [thisData, temp];
        end

        if any(isnan(thisData))
            print("NaN at " + row.name)
        end
        
        evalfun = sprintf( 'out.%s = thisData;', keymap.name(k) );
        eval( evalfun );
    end
end