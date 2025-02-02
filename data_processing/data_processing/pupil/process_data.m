function [] = process_data(dir, in_csv_file, mat_file, data_csv_file, seg_csv_file, plot_data)
    % Read the csv file
    csv = readtable([dir in_csv_file]);

    % Remove erroneous data at the beginning of the csv
    start_idx = 1;
    while csv.TIME(start_idx) == 0
        start_idx = start_idx + 1;
    end
    
    % Initialize variables
    t_ms = [csv.TIME(start_idx) * 1000];
    L = [csv.LPD(start_idx)];
    R = [csv.RPD(start_idx)];
    segment_start = [csv.TIME(start_idx)];
    segment_end = [];
    segment_name = {char(csv.MEDIA_NAME(start_idx))};

    % Iterate over csv
    for r = start_idx+1:height(csv)
        % Add new segments when the media name changes
        name = char(csv.MEDIA_NAME(r));
        if ~ismember(name, segment_name)
            end_time = segment_start(end) + csv.TIME(r-1);
            segment_start(end+1) = end_time + csv.TIME(r-1) - csv.TIME(r-2);
            segment_end(end+1) = end_time;
            segment_name(end+1) = {name};
        end

        % Add time (in ms), LPD, and RPD to respective variables
        t_ms(end+1) = (segment_start(end) + csv.TIME(r)) * 1000;
        L(end+1) = csv.LPD(r);
        R(end+1) = csv.RPD(r);

        % Make sure the times are at least 1 ms apart
        if t_ms(end-1) > t_ms(end) - 1
            t_ms(end) = t_ms(end-1) + 1;
        end
    end
    % Add the final segment
    segment_end(end+1) = segment_start(end) + csv.TIME(end);
    
    % Create data structures for RawFileModle
    diameterUnit = 'pxl';
    diameter = struct('t_ms', t_ms', 'L', L', 'R', R');
    
    segmentStart = segment_start';
    segmentEnd = segment_end';
    segmentName = string(segment_name');
    segmentsTable = table(segmentStart, segmentEnd, segmentName);
    
    % Create RawFileModel to be used as input to PupilDataModel
    rfm = RawFileModel(diameterUnit, diameter, segmentsTable);
    rfm.saveMatFile([dir mat_file])

    % Get the setting for the PupilDataModel
    settings = PupilDataModel.getDefaultSettings();
    settings.raw.PupilDiameter_Max = inf;
    settings.raw.PupilDiameter_Min = 12;
    settings.raw.dilationSpeedFilter_MadMultiplier = 4;
    settings.raw.residualsFilter_MadMultiplier = 4;

    % Create the PupilDataModel
    pdm = PupilDataModel(dir, mat_file, settings);

    % Process the pupil data
    pdm.filterRawData();
    pdm.processValidSamples();

    % Get the processed mean pupil diameters
    times = pdm.(['mean' 'Pupil_ValidSamples']).samples.t_ms;
    diameters = pdm.(['mean' 'Pupil_ValidSamples']).samples.pupilDiameter;
    data_table = table(times, diameters);

    % Save the results to 2 csv files
    writetable(data_table, [dir data_csv_file]);
    writetable(segmentsTable, [dir seg_csv_file]);

    if plot_data==true
        % Plot the pupil processing
        pdm.plotData;
    end
end
